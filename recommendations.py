import pandas as pd
import numpy as np
import pickle
import torch
from ncf_model import NCF
import random

from surprise import Dataset
from surprise.reader import Reader
from surprise.prediction_algorithms.matrix_factorization import SVD as FunkSVD


def ncf_model_predictions(test_user, ncf_df):

    # get num users and games and list of all game ids
    num_users = ncf_df['user_id'].max()+1
    num_items = ncf_df['app_id'].max()+1
    all_game_ids = ncf_df['app_id'].unique()

    # instantiate the model in the evaluation state
    ncf_model = NCF(num_users, num_items, ncf_df, all_game_ids)
    ncf_model.load_state_dict(torch.load('ncf_model.pth'))
    ncf_model.eval()

    # Dict of all items that are interacted with by each user
    user_interacted_items = ncf_df.groupby('user_id')['app_id'].apply(list).to_dict()

    # get candidate games for user
    test_users_games = user_interacted_items.get(test_user, [])
    candidate_games = list(set(all_game_ids) - set(test_users_games))
    test_user = torch.tensor([test_user]*len(candidate_games))
    candidate_games = torch.tensor(candidate_games)

    # get predictions
    with torch.no_grad():
        predictions = ncf_model(test_user, candidate_games)

    # sort top 100 games and randomly select 10
    _, sorted_indices = torch.topk(predictions.view(-1), 100, largest=True)

    random_10 = sorted_indices[torch.randperm(100)[0:10]]

    top10_appIDs = candidate_games[random_10].tolist()

    return top10_appIDs


def svd_model_predictions(test_user, svd_df):
    
    # find the unplayed games
    played_games = svd_df[svd_df['user_id'] == test_user]
    played_games = played_games['app_id'].tolist()
    all_games_list = svd_df['app_id'].unique().tolist()
    unplayed_games = [game for game in all_games_list if game not in played_games]

    with open('svd_model.pkl', 'rb') as file:
        svd_model = pickle.load(file)

    # preparing the data for our model
    my_dataset = Dataset.load_from_df(svd_df, Reader(rating_scale=(0, 1)))
    my_train_dataset = my_dataset.build_full_trainset()

    predictions = []

    for game in unplayed_games:
        # get predictions
        prediction = svd_model.predict(test_user, my_train_dataset)
        predictions.append((game,prediction))

    # Get the top 10 appIDs (games) from the sorted predictions
    sorted_predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
    top100_appIDs = [prediction[0] for prediction in sorted_predictions[:100]]

    top10_appIDs = random.sample(top100_appIDs, k=10)

    return top10_appIDs


def get_cold_start_recs(game_info_df):

    top10_appIDs = game_info_df['app_id'].sample(n=10).tolist()

    # titles = [
    #     'Call of Duty: Modern Warfare 2 (2009)',
    #     'JoJos Bizarre Adventure: All-Star Battle R',
    #     'FATAL FRAME / PROJECT ZERO: Maiden of Black Water',
    #     'Zombie Army 4: Dead War',
    #     'Forager',
    #     '武侠乂 The Swordsmen X'
    # ]
    # header_images = [
    #     'https://cdn.akamai.steamstatic.com/steam/apps/10180/header.jpg?t=1654809646',
    #     'https://cdn.akamai.steamstatic.com/steam/apps/1372110/header.jpg?t=1666908137',
    #     'https://cdn.akamai.steamstatic.com/steam/apps/1732190/header.jpg?t=1663081460',
    #     'https://cdn.akamai.steamstatic.com/steam/apps/694280/header.jpg?t=1652368094',
    #     'https://cdn.akamai.steamstatic.com/steam/apps/751780/header.jpg?t=1667237775',
    #     'https://cdn.akamai.steamstatic.com/steam/apps/840140/header.jpg?t=1588046169'
    # ]
    # prices = [
    #     '19.99',
    #     '49.99',
    #     '29.99',
    #     '49.99',
    #     '19.99',
    #     '24.99'
    # ]
    return top10_appIDs


def game_details(top10_appIDs, game_info_df):

    game_details = game_info_df.loc[game_info_df['app_id'].isin(top10_appIDs)]

    titles = []
    header_images = []
    prices = []
    for id in top10_appIDs:
        title = game_details['title'].loc[game_details['app_id'] == id].values
        header_image = game_details['header_image'].loc[game_details['app_id'] == id].values
        price = game_details['price'].loc[game_details['app_id'] == id].values

        titles.append(title)
        header_images.append(header_image)
        prices.append(price)

    titles = np.array(titles).flatten().tolist()
    header_images = np.array(header_images).flatten().tolist()
    prices = np.array(prices).flatten().tolist()
    prices = [round(value, 2) for value in prices]

    return titles, header_images, prices
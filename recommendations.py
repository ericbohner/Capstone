import pandas as pd
import numpy as np
import torch
from ncf_model import NCF


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


# print(ncf_model_predictions(3046002))

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

    # names = [
    #     'Call of Duty: Modern Warfare 2 (2009)',
    #     'JoJos Bizarre Adventure: All-Star Battle R',
    #     'FATAL FRAME / PROJECT ZERO: Maiden of Black Water',
    #     'Zombie Army 4: Dead War',
    #     'Forager',
    #     '武侠乂 The Swordsmen X'
    # ]
    # prices = [
    #     '19.99',
    #     '49.99',
    #     '29.99',
    #     '49.99',
    #     '19.99',
    #     '24.99'
    # ]
    return titles, header_images, prices


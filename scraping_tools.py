from steam import Steam
from decouple import config
import pandas as pd
import json

KEY = config("STEAM_API_KEY")

steam = Steam(KEY)

def steam_user_info(steamid):
    '''
    Returns a list with the steam username, profile URL, and date created

    Args:
        steamid: a string of the user's Steam ID

    Returns:
        user_info: a DataFrame containing the following columns:
            'personaname',
            'profile_url',
            'timecreated'
    '''
    user_details = steam.users.get_user_details(steamid)

    personaname = user_details['player']['personaname']
    profile_url = user_details['player']['profileurl']
    time_created = user_details['player']['timecreated']

    # user_info = [personaname, profile_url, time_created]

    return personaname, profile_url, time_created

def recently_played_games(steamid):
    '''
    Finds the user's recently played games and returns a pandas DataFrame containing
    relevant details about those games.

    Args:
        steamid: a string of the user's Steam ID

    Returns:
        recently_played_df: a DataFrame containing the following columns:
            'appid',
            'name',
            'playtime_2weeks',
            'playtime_forever'
    '''
    recently_played = steam.users.get_user_recently_played_games(steamid)
    df = pd.DataFrame(recently_played['games'])
    required_columns = ['appid', 'name', 'playtime_2weeks', 'playtime_forever']
    recently_played_df = df[required_columns]
    return recently_played_df


def steam_library(steamid):
    '''
    Gets the entire steam library as a DataFrame from the user along with hours played.

    Args:
        steamid: a string of the user's Steam ID

    Returns:
        user_library: a DataFrame containing the following columns:
            appid,
            playtime_forever,
            user_id
    '''
    user_library = steam.users.get_owned_games(steamid)
    game_data = user_library['games']
    app_data = []
    for game in game_data:
        app_id = game['appid']
        playtime_forever = game['playtime_forever']
        app_data.append({'app_id': app_id, 'hours': playtime_forever})
    library = pd.DataFrame(app_data)
    library['user_id'] = int(steamid)
    return library

def get_game_details(gameid):
    '''
    Returns a dict with details for a given gameid

    Args:
        gameid: string game/app id

    Returns:
        game_details: a data dictionary that includes details about the game
    '''
    game_details = steam.apps.search_games(gameid)
    return game_details

def get_app_pubs_devs(gameid):
    '''Return app publisher and developer'''
    details = steam.apps.get_app_details(gameid)
    details_dict = json.loads(details)
    
    app_data = details_dict.get(str(gameid), {}).get('data', {})
    publishers = app_data.get('publishers', [])
    developers = app_data.get('developers', [])

    return publishers, developers

def get_user_app_stats(steamid, app_id):
    '''Returns a user's stats for a particular game'''
    user_app_stats = steam.apps.get_user_stats(steamid, app_id)
    return user_app_stats

#### TESTING FUNCTIONS ####
# userid = '76561198120441502'
# userid2 = '76561198018875258'
# appid = '1868140'

# print(get_game_details('304390'))


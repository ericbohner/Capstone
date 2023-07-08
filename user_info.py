from steam import Steam
from decouple import config
import pandas as pd

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

    user_info = [personaname, profile_url, time_created]

    return user_info

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
    Gets the entire steam library from the user along with hours played.
    Sorted by most played to least played.

    Args:
        steamid: a string of the user's Steam ID

    Returns:
        user_library: a DataFrame containing the following columns:
            appid,
            name,
            playtime_2weeks,
            playtime_forever
    '''
    user_library = steam.users.get_owned_games(steamid)
    return user_library

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

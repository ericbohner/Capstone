from user_info import steam_user_info
from user_info import recently_played_games
from user_info import steam_library
from user_info import get_game_details

import pandas as pd

def game_details():
    names = [
        'SurReal Subway',
        'Battle Motion',
        'Game Name',
        'Star Wars',
        'Other Game',
        'Genshin Impact'
    ]
    prices = [
        '9.99',
        '10.01',
        '93.21',
        '9.34',
        '3.00',
        'FREE'
    ]
    return names, prices


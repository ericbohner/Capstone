from scraping_tools import steam_user_info
from scraping_tools import recently_played_games
from scraping_tools import steam_library
from scraping_tools import get_game_details

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


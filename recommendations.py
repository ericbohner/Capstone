from scraping_tools import steam_user_info
from scraping_tools import recently_played_games
from scraping_tools import steam_library
from scraping_tools import get_game_details

import pandas as pd

def game_details():
    names = [
        'Call of Duty: Modern Warfare 2 (2009)',
        'JoJos Bizarre Adventure: All-Star Battle R',
        'FATAL FRAME / PROJECT ZERO: Maiden of Black Water',
        'Zombie Army 4: Dead War',
        'Forager',
        '武侠乂 The Swordsmen X'
    ]
    prices = [
        '19.99',
        '49.99',
        '29.99',
        '49.99',
        '19.99',
        '24.99'
    ]
    return names, prices


# UI requirements
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.label import MDLabel

# data manipulation
import datetime
import webbrowser
import pandas as pd

# Steam API requirements
from scraping_tools import steam_user_info
from recommendations import game_details
from recommendations import ncf_model_predictions

# GF: 76561198120441502
# BF: 76561198018875258

# setting the window size
Window.size = (600, 750)

# read in important csvs
ncf_df = pd.read_csv('data/ncf_recommendations.csv')
game_info_df = pd.read_csv('data/game_details.csv')

class MainScreen(MDScreen):
    
    # set text for initial labels
    personaname = StringProperty("")
    profile_url = StringProperty("")
    time_created = StringProperty("")
    steam_id = StringProperty("") 

    def get_steam_id(self, instance):
        '''
        Gets the user's steam id from the MDTextField 'steam_id_input'.
        Then calls the functions that get the rest of the information for the app.
        '''
        steam_id = instance.text
        self.get_user_info(steam_id)
        self.get_recommendations(steam_id)

    def get_user_info(self, steam_id):
        '''Find user_info from steam_id'''
        pass
        # self.user_info = steam_user_info(steam_id)
        # self.personaname, self.profile_url, self.created_date = self.user_info
        # self.time_created = str(datetime.datetime.fromtimestamp(self.created_date))

    def get_recommendations(self, steam_id):
        '''Gets user's game recommenations'''
        user_id = int(steam_id)
        top10_appIDs = ncf_model_predictions(test_user=user_id, ncf_df=ncf_df)
        print(top10_appIDs)
        top10_titles, header_images, prices = game_details(top10_appIDs, game_info_df)
        print(top10_titles, header_images, prices)
        self.create_recommendations(top10_titles, header_images, prices)

    def create_recommendations(self, top10_titles, header_images, prices):
        '''Clear existing recommentations and create new recommendations'''

        self.ids.image_grid.clear_widgets()

        for i in range(6):
            url = 'https://steamcommunity.com/id/afishnamedfish/'
            img = header_images[i]
            title = top10_titles[i]
            price = prices[i]
            self.create_smart_tile(url, img, title, price)

    def create_smart_tile(self, url, img, title, price):
        '''Add MDSmartTile widgets to the image_grid MDStackLayout'''

        # creating the image tile
        self.rec_list_item = MDSmartTile(
            radius=[14, 14, 0, 0],
            box_radius=[0, 0, 14, 14],
            box_color=[0, 151, 222, .2],
            overlap=False,
            source=img,
            pos_hint={"center_x": .5, "center_y": .5},
            size_hint=(None, None),
            size=("240dp", "135dp"),
            on_release=lambda url=url: self.open_link(url)
        )

        # two labels for the image tile
        rec_label = MDLabel(
            text=title,
            bold=True
        )
        price_label = MDLabel(
            text=str(price),
            bold=True,
            size_hint=(0.5, 1),
            halign='right'
        )

        # add icon and label widget to the image tile
        self.rec_list_item.add_widget(rec_label)
        self.rec_list_item.add_widget(price_label)
        # add the image tile to the MDStackLayout
        self.ids.image_grid.add_widget(self.rec_list_item)

    def open_link(self, url):
        '''open url in browser'''
        webbrowser.open(url)
        
class RecommenderApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Dark'

        return Builder.load_file('recommenderui.kv')
    
if __name__ == '__main__':
    RecommenderApp().run()

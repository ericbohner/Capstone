Steam Game Recommendation System Project 
by: Eric Bohner

Created for BrainStation Capstone Project 

The project has four main parts:
    - Data Collection and Cleaning
    - Exploratory Data Analysis
    - Modelling
    - Implementation of the Recommender in a UI

The first three parts are contained in their corresponding jupyter notebooks (.ipynb files).

The UI is spread across the following files:
    - main.py
    - recommendations.py
    - scraping_tools.py
    - recommenderui.kv

The recommenderui.kv contains the styling for the UI.  It defines the layout, colours, and styles for the app.

scraping_tools.py contains all of the operations that use the Steam API to collect user and game data.  The main 
use case for this is to find the user's game library and hours played so that predictions can be made for which 
games they would enjoy.  

recommendations.py contains the final trained model that is used to make predictions.

main.py collects all of the contents from the other UI files and adds functionality to the UI.
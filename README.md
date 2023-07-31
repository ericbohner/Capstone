# Steam Game Recommendation System Project 
by: Eric Bohner

Created for BrainStation Capstone Project 

## Introduction

For this project I built a functioning game recommendation system app that provides recommendations
to users from an existing dataset of games according to three different models: a content-based model,
which determines popular and similar games; an SVD model, which attempts to determine user preferences
from a user-item matrix; and a neural collaborative filtering model, which takes user and item
embeddings to determine user preferences.  These models are presented in a custom-built front end 
that takes in a User ID to determine user preferences according to the selected model.

Here is an example of the UI providing recommendations to a user:


![image](https://github.com/ericbohner/Capstone/assets/131715470/4861f2ec-3fea-42c9-b6e5-f3a3833f30fa)



## Contents

- Data Collection and Cleaning
- Exploratory Data Analysis
- Modelling
    - Content based filtering
    - Funk Singular Value Decomposition (SVD)
    - Neural Collaborative Filtering (NCF)
- Implementation of the Recommender in a UI

## Data Collection and Cleaning

All preliminary data collection and cleaning was done in the data_cleaning.ipynb.

data_cleaning.ipynb includes the cleaning process for several datasets:
- games.csv (providing game details. games_metadata.json provided tag details)
- users.csv (showing how many reviews a user had given and how many products they owned)
- recommendations.csv (containing user reviews for specific games)
- steam_games.csv (game details including publisher, developer, etc.)

the steam_games.csv dataset was eventually abandoned in favour of combining the games.csv
and games_metadata.json files to get one-hot encoded game data.

## Exploratory Data Analysis

EDA.ipynb includes some preliminary observations from the dataset, such as the most frequently
occurring tags, popular release dates, and other various statistics of interest.

## Modelling

In this project I created three models: a content-based filtering system, a FunkSVD model, and
a deep learning Neural Collaborative Filtering model.  All of the preproccessing, training, and
testing was done in their corresponding notebooks:
- content_model.ipynb
- funksvd_model.ipynb
- ncf_model.ipynb

### Content Based Modelling

The content-based model was developed as a rough-and-ready method for handling the Cold Start
Problem.  It determines popular games based on a game's positve ratio, release date, and 
number of reviews in order to provide a list of games that are likely to be enjoyed by the 
largest majority of individuals.

### FunkSVD Modelling

Supposing the user can be found in the collected dataset, this model determines user preferences
in a user-item matrix by performing an SVD matrix factorization.  It takes in users' ratings of 
different games to determine user similarities and game similarities.  From that, it fills in 
predicted ratings for each user-item pair.  To make predictions, these predicted ratings are
ordered from highest to lowest to find the games with the best "fit" for users.

In the UI, 6 of the top 50 are randomly selected to be displayed to the user, preventing the user
from receiving the same 6 recommendations each time.

### NCF Modelling

Here, a neural collaborative filtering model was created to perform a more comprehensive assessment
of user-item preferences.  User and Item embeddings were created for each user before being concatenated
and processed to identify how a user interacts with different games.  To assess this model, a Hit 
Ratio @ 10 was used to identify whether the model could accurately identify a user's known positively
rated game from a random selection of unknown games.


## Front End / UI

The UI is mainly spread across the following files:
- main.py
- recommendations.py
- scraping_tools.py
- recommenderui.kv
In addition to these files, there are also two other .py files that 
contain the trained models used for making user predictions:
- ncf_model.py (which reads in ncf_model.pth)
- svd_model.py (which reads in svd_model.pkl)

The UI files perform the following tasks:

main.py collects all of the contents from the other UI files and adds functionality to the UI.

The recommenderui.kv contains the styling for the UI.  It defines the layout, colours, styles, 
buttons, etc. for the app.

scraping_tools.py contains all of the operations that use the Steam API to collect user and 
game data.  The main use case for this is to find the user's steam link to link to the user's 
profile. It was also used to impute some missing data from the steam_games dataset.  

recommendations.py reads in the trained models, training datasets, and user information in order 
to make predictions for a specific user.  As part of the processing, it generates header images,
prices, and game titles which are passed back to main.py for being displayed in the app.


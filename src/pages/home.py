"""
ICS3U 
Eric Sui
This file contains the code for the layout of the home page
"""

# Import dash libraries for components
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import json library to access JSON files
import json

# Import the custom defined functions stored in funcs.py 
from pages.funcs import fetch

# Opening the config.json file to get the name of the user
with open("./config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

# Acessing the first and last name from the json file
firstName = jsonObject["firstName"]
lastName = jsonObject["lastName"]

# Setting up the color scheme for this layout
colors = {
    'background': '#111111',
    'text': '#363636'
}

# Here, we declared two lists. One contains important the S&P, Dow Jones, and Nasdaq Composite and the other list is going to contain the cards
importantStocks = [['^GSPC', '^DJI', '^IXIC'], ['S&P 500', 'Dow Jones Industrial Average', 'NASDAQ Composite']]

cardsList = []

# This for loop makes three cards: one for each of the important stocks.
for i in range(0, 3):
    # This puts the stock that we're dealing with now into a variable so we don't have to type importantStocks[0][i] a bunch of times.
    stock = importantStocks[0][i]

    # Get the figure object and information needed through the function defined in fetch.py
    fig, infor = fetch.homePage(stock)

    # Create the text displayed on the card
    cardText = html.H5(f"{importantStocks[1][i]}:\n{float(infor[0])}$")
    
    # Add the card to the list as defined by the bootstrap components
    cardsList.append(
        dbc.Card(
            [
                # Add the graph as the header of the card
                dcc.Graph(figure=fig),
                # Display the information in the text of the card
                dbc.CardBody(
                    [
                        html.H4(cardText),
                        html.H6(f"Day High: {infor[3]}"),
                        html.H6(f"Day Low: {infor[4]}"),
                        html.H6(f"52 Week High: {infor[5]}"),
                        html.H6(f"52 Week Low: {infor[6]}")
                    ]
                )
            ],
            # Green outline
            color = "success",
            outline = True
        )
    )

# Define a variable that contains a div of the three cards
cards = html.Div(
    # Make a bootstrap row with all the cards for scalability 
    children = dbc.Row(
        [
            dbc.Col(cardsList[0]), 
            dbc.Col(cardsList[1]),
            dbc.Col(cardsList[2])
        ]
    ),
    # Add 30px margins to the left and right
    style = {
        'margin-left' : '30px',
        'margin-right' : '30px'
    }
)

# Layout variable which contains the display for the page and div with all content to be shown
layout = html.Div(
    children=[
        # Header for the name and greeting
        html.H1(
            children=f"Welcome, {firstName} {lastName}",
            # Align the text to the center of the page and use color as defined in the dictionary
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        # Header to explain what the cards are about
        html.H2(
            children='Important Stocks', 
            # Align the text to the left, use color as defined in dictionary, add 30px margins to left and top
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'margin-left': '30px',
                'margin-top': '30px'
            }),
        # Display the card components which are stored in the array
        cards
    ]
)

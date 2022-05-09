import json

import dash
from dash import Input, Output, State, html, dcc

import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd

import numpy as np
from pandas_datareader import data as pdr 
import plotly.graph_objs as go 
import yfinance as yf

from pages.funcs import fetch

with open("./config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

firstName = jsonObject["firstName"]
lastName = jsonObject["lastName"]

colors = {
    'background': '#111111',
    'text': '#363636'
}

trendingStocks = [['^GSPC', '^DJI', '^IXIC'], ['S&P 500', 'Dow Jones Industrial Average', 'NASDAQ Composite']]
cardsList = []
for i in range(0, 3):
    
    stock = trendingStocks[0][i]

    fig, infor = fetch.homePage(stock)

    cardText = html.H5(f"{trendingStocks[1][i]}:\n{float(infor[0])}$")
    
    cardsList.append(dbc.Card(
        [
            dcc.Graph(figure=fig),
            dbc.CardBody([

            
                html.H4(cardText),
                html.H6(f"Day High: {infor[3]}"),
                html.H6(f"Day Low: {infor[4]}"),
                html.H6(f"52 Week High: {infor[5]}"),
                html.H6(f"52 Week Low: {infor[6]}")
            ]
            )
        ],
        color = "success",
        outline = True
    ))
cards = html.Div(
    children = dbc.Row([
        dbc.Col(cardsList[0]), 
        dbc.Col(cardsList[1]),
        dbc.Col(cardsList[2])
    ]),
    style = {
        'margin-left' : '30px',
        'margin-right' : '30px'
    }
)

layout = html.Div(children=[
    html.H1(
        children=f"Welcome, {firstName} {lastName}",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.H2(children=' ', style={
        'textAlign': 'left',
        'color': colors['text'],
        'margin-left': '30px',
        'margin-top': '30px'
    }),
    cards
])

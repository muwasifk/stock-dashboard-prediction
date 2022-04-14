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
    yf.pdr_override()
    stock = trendingStocks[0][i]
    df = yf.download(tickers=stock,period='3mo',interval='1d')

    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    fig.update_layout(
        yaxis_title='Price (USD/Share)', xaxis_rangeslider_visible=False)               

    infor = yf.Ticker(trendingStocks[0][i]).info

    cardText = html.H5(f"{trendingStocks[1][i]}:\n{int(infor['regularMarketPrice'])}$")
    
    cardsList.append(dbc.Card(
        [
            dcc.Graph(figure=fig),
            dbc.CardBody([

            
                html.H4(cardText),
                html.H6(f"Day High: {infor['dayHigh']}"),
                html.H6(f"Day Low: {infor['dayLow']}"),
                html.H6(f"52 Week High: {infor['fiftyTwoWeekHigh']}"),
                html.H6(f"52 Week Low: {infor['fiftyTwoWeekLow']}")
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

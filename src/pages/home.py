import json
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.express as px
import pandas as pd
# Market Data 
import yfinance as yf

df = px.data.stocks()
fig = px.line(df, x='date', y="GOOG")

with open("./config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

firstName = jsonObject["firstName"]
lastName = jsonObject["lastName"]

colors = {
    'background': '#111111',
    'text': '#363636'
}


trendingStocks = [['/static/images/placeholder286x180.png', '/static/images/placeholder286x180.png', '/static/images/placeholder286x180.png'], ['AAPL', 'TSLA', 'GME'], ['600$', '800$', '200$']]
cardsList = []
for i in range(0, 3):
    cardText = html.H2(f"{trendingStocks[1][i]}: {trendingStocks[2][i]}")
    
    cardsList.append(dbc.Card(
        [
            dcc.Graph(figure=fig),
            dbc.CardBody(
                html.H4(cardText)
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
    html.H2(children='Trending Stocks', style={
        'textAlign': 'left',
        'color': colors['text'],
        'margin-left': '30px',
        'margin-top': '30px'
    }),
    cards
])

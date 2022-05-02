import json
import dash_bootstrap_components as dbc
from dash import html
import yfinance as yf

with open("pages/watchlist.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

portfolioStocks = jsonObject["watchlistStocks"]

table_header = [
    html.Thead(
        html.Tr(
            [
                html.Th("Ticker"), 
                html.Th("Current (USD)"), 
                html.Th("Open (USD)"), 
                html.Th("High (USD)"), 
                html.Th("Low (USD)"), 
                html.Th("52W High (USD)"), 
                html.Th("52W Low (USD)")
            ]
        )
    )
]

rows = []

for i in range(0, len(portfolioStocks)):
    curData = yf.Ticker(portfolioStocks[i]).info 

    rows.append(
        html.Tr(
            [
                html.Td(portfolioStocks[i]),
                html.Td(curData['regularMarketPrice']),
                html.Td(curData['open']),
                html.Td(curData['dayHigh']),
                html.Td(curData['dayLow']),
                html.Td(curData['fiftyTwoWeekHigh']),
                html.Td(curData['fiftyTwoWeekLow'])
            ]
        )
    )

table_body = [html.Tbody(rows)]

table = dbc.Table(table_header + table_body, bordered = False, striped = True, hover=True)

layout = html.Div(children=[
    html.H1(
        children="WATCHLIST",
        style = {
            'text-align': 'center',
            'color': '#4db6ac',
            'font-family': 'Montserrat'
        }),
    html.Div(
        children = table,
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        }
    ) 
], id='page-content')


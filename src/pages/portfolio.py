from dataclasses import replace
import json
import dash_bootstrap_components as dbc
from dash import html, Output, Input, dcc
import yfinance as yf
import datetime

from pages.funcs import fetch

colors = {
    'background': '#111111',
    'text': '#363636'
}

def formtable():
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    portfolioStocks = jsonObject["portfolioStocks"]
 
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("Ticker"),
                    html.Th("Current Price"),
                    html.Th("Buy Price"),
                    html.Th("Volume"),
                    html.Th("Profit"),
                    html.Th("Date Bought")
                ]
            )
        )
    ]

    totalProfit = 0
    totalBalance = 0

    rows=[]

    for i in range(1, len(portfolioStocks)):
        currentStock = portfolioStocks[i]
        ticker = currentStock[0]
        currentPrice = float(fetch.portfolioFetchData(ticker).replace(",",""))
        buyPrice = 600
        volume = currentStock[1]
        profit = (currentPrice - buyPrice) * volume
        dateBought = currentStock[2]
        totalBalance += currentPrice*volume
        totalProfit += profit

        rows.append(html.Tr([
            html.Td(ticker),
            html.Td(f"{currentPrice}$"),
            html.Td(f"{buyPrice}$"),
            html.Td(str(volume)),
            html.Td(f"{profit}$"),
            html.Td(dateBought)
        ]))

    table_body = [html.Tbody(rows)]

    table = dbc.Table(table_header + table_body, striped = True, hover = True, id="tabletable")

    return table 

table = formtable()

layout = html.Div(children = [
    html.H1(
        children = "YOUR PORTFOLIO",
        style = {
            'text-align': 'center',
            'color': '#4db6ac',
            'font-family': 'Montserrat'
        }
    ),
    html.Div(
        children = table,
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        }
    ),
], id='page-content')


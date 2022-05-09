import json
import dash_bootstrap_components as dbc

from dash import html, Output, State, Input, dcc
import yfinance as yf

from pages.funcs import fetch

from app import app

def formtable():
    with open("pages/watchlist.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    watchlistStocks = jsonObject["watchlistStocks"]

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

    for i in range(0, len(watchlistStocks)):
        curData = fetch.watchlistFetchData(watchlistStocks[i]) 

        rows.append(
            html.Tr(
                [
                    html.Td(watchlistStocks[i]),
                    html.Td(curData[0]),
                    html.Td(curData[1]),
                    html.Td(curData[2]),
                    html.Td(curData[3]),
                    html.Td(curData[4]),
                    html.Td(curData[5])
                ]
            )
        )

    table_body = [html.Tbody(rows)]

    table = dbc.Table(table_header + table_body, bordered = False, striped = True, hover=True)

    return table


layout = html.Div(children=[
    html.H1(
        children="WATCHLIST",
        style = {
            'text-align': 'center',
            'color': '#4db6ac',
            'font-family': 'Montserrat'
        }),
    html.Div(
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        },
        id = 'body-table'
    ),
    
    html.Div(dbc.Button(
        children = 'Refresh Data',
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        },
        id='refresh-button',
        n_clicks=0,  outline=True, color="danger"
    ), 
        className="d-grid gap-2 col-6 mx-auto"),

], id='page-content')

@app.callback(
    Output('body-table', 'children'),
    Input('refresh-button', 'n_clicks')
)
def refreshTable(n_clicks):
    table = formtable()
    return [table]
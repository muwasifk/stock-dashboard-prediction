import json
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.express as px

with open("pages/watchlist.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

portfolioStocks = jsonObject["watchlistStocks"]

table_header = [
    html.Thead(html.Tr([html.Th("Ticker"), html.Th("Open"), html.Th("High"), html.Th("Low"), html.Th("52W High"), html.Th("52W Low")]))
]

row1 = html.Tr([html.Td("AAPL"), html.Td("167.39"), html.Td("170.90"), html.Td("166.78"), html.Td("182.94"), html.Td("122.25")])

table_body = [html.Tbody([row1, row1])]

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
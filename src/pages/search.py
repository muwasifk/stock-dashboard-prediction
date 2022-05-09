import json
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.express as px
from app import app
from pages.funcs import fetch
import plotly.graph_objects as g

text_input = html.Div(
    [
        html.Div(dbc.Input(id="input", placeholder="Ticker", type="text", debounce=True), style = {
            
        }),
        html.Br(),
        html.Div(id="output"),
    ]
)

with open("pages/watchlist.json") as jsonFile:
    currentWatchlist = json.load(jsonFile)['watchlistStocks']
    
    jsonFile.close()

with open("pages/portfolioStocks.json") as jsonFile:
    currentPortfolio = json.load(jsonFile)['portfolioStocks']
    
    jsonFile.close()


layout_output = html.Div(
    [html.Div(id = 'layout-output', style = {})],
    id = 'layout-content'
)

tickerName = []
@app.callback(Output("layout-content", "children"), [Input("input", "value")])
def output_text(value):
    try: 
        fig, fullname, info = fetch.searchData(value)
        returnChild = dbc.Row([
                dbc.Col([fig]),
                dbc.Col([
                    html.H2(f"{fullname}"),
                    html.Br(),
                    html.H3(info[0]), 
                    html.H5(f"Open: {info[1]}"),
                    html.H5(f"High: {info[2]}"),
                    html.H5(f"Low: {info[3]}"),
                    html.H5(f"52W High: {info[4]}"),
                    html.H5(f"52W Low: {info[5]}"),
                ])
            ])
        
        buttons = html.Div(
            [
                dbc.Button("Watchlist +", color="warning", disabled=False, id='watchlist-add'),
                dbc.Button("Portfolio +", color="danger", disabled=False, id='portfolio-add'),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Add to Portfolio"), close_button=True),
                        dbc.ModalBody([dbc.Input(id="volume-input", placeholder="Number of Shares Bought", type="text", debounce = True), dbc.Input(id="buy-date", placeholder="Date Bought (DD/MM/YY)", type="text", debounce = True),]),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Submit",
                                id="submit-button",
                                className="ms-auto",
                                n_clicks=0,
                            )
                        ),
                    ],
                    id="portfolio-popup",
                    centered=True,
                    is_open=False,
                ),

            ], className="d-grid gap-2 col-6 mx-auto"
        )
        tickerName.append(value)
        return [buttons, html.Div([returnChild], id='layout-output', style = {'margin-top' : '30px'})]

    except: 
        if value is not None:
            return [dbc.Toast(
                [html.P("Please enter a valid ticker that can be found on Yahoo Finance", className="mb-0")],
                id="auto-toast",
                header="Invalid Ticker",
                icon="danger",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]


@app.callback(
    Output("portfolio-popup", "is_open"),
    [
        Input("portfolio-add", "n_clicks"), 
        Input("submit-button", "n_clicks")
    ],
    [State("portfolio-popup", "is_open")],
)
def toggle_modal(portfolioClicks, submitClicks, is_open):
    if portfolioClicks or submitClicks:
        return not is_open
@app.callback(
    Output('portfolio-toast', 'children'),
    [
        Input('submit-button', 'n_clicks')
    ]
)

@app.callback(
    Output("watchlist-toast", 'children'),
    [Input('watchlist-add', 'n_clicks')]
)
def updateWatchlist(n):
    if n is not None:
        if tickerName[-1] not in currentWatchlist: 
            currentWatchlist.append(tickerName[-1])
            jsonData={
                "watchlistStocks": currentWatchlist
            }
            with open('pages/watchlist.json', 'w') as jsonFile:
                json.dump(jsonData, jsonFile)
                jsonFile.close()
        else:
            return [dbc.Toast(
                    id="auto-toast",
                    icon="danger",
                    header=f"{tickerName[-1]} is already in your watchlist",
                    duration=2750,
                    is_open=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )]
        return [dbc.Toast(
                id="auto-toast",
                icon="success",
                header="Added to your watchlist",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]
layout = html.Div(children=[
    dbc.Row([
        dbc.Col([]),
        dbc.Col([text_input]),
        dbc.Col([])
    ]),
    dbc.Row([dbc.Col([layout_output])]), 
    html.Div(id = 'watchlist-toast'),
    html.Div(id = 'portfolio-toast')
], id='page-content')
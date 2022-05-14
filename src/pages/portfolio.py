from dataclasses import replace
import json
import dash_bootstrap_components as dbc
from dash import html, Output, Input, State, dcc
import yfinance as yf
import datetime
import plotly.graph_objects as go

from pages.funcs import fetch
from app import app 

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

    for i in range(0, len(portfolioStocks)):
        currentStock = portfolioStocks[i]
        ticker = currentStock[0]
        currentPrice = float(fetch.portfolioFetchData(ticker).replace(",",""))
        buyPrice = currentStock[3]
        volume = currentStock[1]
        profit = (currentPrice - buyPrice) * volume
        dateBought = currentStock[2]
        totalBalance += currentPrice*volume
        totalProfit += profit

        rows.append(html.Tr([
            html.Td(ticker),
            html.Td(f"{currentPrice}$"),
            html.Td(f"{buyPrice}$"),
            html.Td(f"{volume}"),
            html.Td(f"{profit}$"),
            html.Td(dateBought)
        ]))

    table_body = [html.Tbody(rows)]

    table = dbc.Table(table_header + table_body, striped = True, hover = True, id="tabletable")

    return table 

def formPieChartVolume():
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    portfolioStocks = jsonObject["portfolioStocks"]

    labels = []
    values = []

    for i in range(0, len(portfolioStocks)):
        labels.append(portfolioStocks[i][0]) 
        values.append(portfolioStocks[i][1])

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, title = 'Volume Composition')])
    fig.update_layout(
    width=450,
    height=450)
    return fig 

def formPieChartProfit():
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    portfolioStocks = jsonObject["portfolioStocks"]

    labels = []
    values = []

    for i in range(0, len(portfolioStocks)):
        labels.append(portfolioStocks[i][0])
        profit = int(float(fetch.portfolioFetchData(portfolioStocks[i][0]).replace(",",""))) * portfolioStocks[i][1]
        values.append(profit)

    print(labels)
    print(values)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, title = 'Value Composition')])
    fig.update_layout(
    width=450,
    height=450)
    return fig 

def formbarchart():
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    portfolioStocks = jsonObject["portfolioStocks"]
    
    industryCounts = {}

    x = []; y = []

    for i in range(0, len(portfolioStocks)):
        if len(portfolioStocks[i]) == 5:

            if portfolioStocks[i][0] not in industryCounts.keys():
                industryCounts[portfolioStocks[i][4]] = 1 
            else:
                industryCounts[portfolioStocks[i][4]] += 1 

    for i in industryCounts.keys():
        x.append(i); y.append(industryCounts[i])
    
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(
        width = 300
    )

    return fig

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
        children = [
            dbc.Row(
                [dbc.Col(
                    dcc.Graph(id = "volumepie"),
                    style = {
                        'margin-left' : '30px'
                    }
                ),
                dbc.Col(
                    dcc.Graph(id = 'profitpie'),
                    style = {
                        'margin-right' : '30px'
                    }
                )]
            ),
            dbc.Row(
                dcc.Graph(id = "industrybar")
            )
        ],
        id = "piegraphs"
    ),
    
    html.Div(
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        },
        id = 'body-table2'
    ),

    html.Div(
        children = [dbc.Row([
            dbc.Col(children = dbc.Button(
                children = 'Refresh Data',
                id='refresh-button2',
                style = {
                    'text-align': 'center'
                },
                n_clicks=0,  outline=True, color="success"
            ), width=6),
            dbc.Col(children = dbc.Button(
                children = 'Remove stock',
                style = {
                    'text-align': 'center'
                },
                id='remove-button',
                n_clicks=0,  outline=True, color="danger"
            ), width=6)]
        )],
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        }
    ),

    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Remove a stock"), close_button=True),
            dbc.ModalBody([
                dbc.Input(id="removed-stock", placeholder="Stock ticker (in caps)", type="text", debounce = True),
                dbc.Input(id="removed-stock-volume", placeholder="Amount of stocks to remove", type="number", debounce = True)
            ], id = "portfolio-remove-modal"),


            dbc.ModalFooter(
                dbc.Button(
                    "Submit",
                    id="submit-button",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="remove-popup-portfolio",
        centered=True,
        is_open=False,
    ),
    html.Div(id = 'remove-toast')
])

@app.callback(
    Output('body-table2', 'children'),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshTable(n_clicks):
    if n_clicks is not None:
        table = formtable()
        return [table]

@app.callback(
    Output('remove-popup-portfolio', 'is_open'),
    [Input('remove-button', 'n_clicks'),
    Input('submit-button', 'n_clicks')],
    [State('remove-popup-portfolio', 'is_open')]
)
def removePopup(removeClicks, submitClicks, is_open):
    if removeClicks or submitClicks:
        return not is_open
@app.callback(
    Output('remove-toast', 'children'),
    [
        Input('submit-button', 'n_clicks'),
        Input('removed-stock', 'value'),
        Input('removed-stock-volume', 'value')
    ]
)
#TODO: ERROR CHECKING IN PORTFOLIO after the try
def removePortfolioStock(clicks, ticker, removedNum):
    if removedNum is not None:
        if int(removedNum) <= 0:
            return [dbc.Toast(
                id="error-toast",
                icon="danger",
                header=f"Invalid ticker volume (negative input detected). Try Again.",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]
    try:
        ticker = str(ticker).upper()
        if clicks is not None:
            with open("pages/portfolioStocks.json") as jsonFile:
                jsonObject = json.load(jsonFile)
                jsonFile.close()
            portfolioStocks = jsonObject["portfolioStocks"]
            newPortfolioStocks = []
            removedNum /= 2
            for i in range(0, len(portfolioStocks)):
                if portfolioStocks[i][0] != ticker:
                    newPortfolioStocks.append(portfolioStocks[i])
                else:
                    if removedNum > 0:
                        if removedNum >= portfolioStocks[i][1]:
                            removedNum -= portfolioStocks[i][1]
                        else:
                            portfolioStocks[i][1] -= removedNum
                            removedNum = 0
                            newPortfolioStocks.append(portfolioStocks[i])
    
            if removedNum > 0:
                return [dbc.Toast(
                    id="error-toast",
                    icon="danger",
                    header=f"Invalid ticker volume. Try Again.",
                    duration=2750,
                    is_open=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )]
            
            else:
                jsonObject = {'portfolioStocks': newPortfolioStocks}
                with open('pages/portfolioStocks.json', 'w') as jsonFile:
                            json.dump(jsonObject, jsonFile)
                            jsonFile.close()
    except:
        if removedNum is not None:
            return [dbc.Toast(
                id="error-toast",
                icon="danger",
                header=f"Invalid ticker name. Try Again.",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]

@app.callback(
    Output("volumepie", "figure"),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshVolumePie(n_clicks):
    if n_clicks is not None: 
        fig = formPieChartVolume()
        return fig

@app.callback(
    Output("profitpie", "figure"),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshProfitPie(n_clicks):
    if n_clicks is not None: 
        fig = formPieChartProfit()
        return fig

@app.callback(
    Output("industrybar", "figure"),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshVolumePie(n_clicks):
    if n_clicks is not None: 
        fig = formbarchart()
        return fig
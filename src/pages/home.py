from dash import html, dcc
import dash_bootstrap_components as dbc
import json
from pages.funcs import fetch

# Opening the config.json file to get the name of the user
with open("./config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

# Acessing the first and last name from the json file
firstName = jsonObject["firstName"]
lastName = jsonObject["lastName"]

# This is setting up the color scheme for this layout
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

    #
    fig, infor = fetch.homePage(stock)

    cardText = html.H5(f"{importantStocks[1][i]}:\n{float(infor[0])}$")
    
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

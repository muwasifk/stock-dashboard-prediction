"""
ICS3U 
Muhammad Wasif Kamran & Eric Sui 
This file contains the code needed for the search page and its functionalities. This was also a very complex page and was a joint effort. Most of the code was written by Wasif and the code written by Eric has been explicitly mentioned with "Written by Eric."
"""

# Importing json to manage storage in JSON files 
import json

# Imports to find UNIX and current time stamps for historical data
import datetime
import time

# Importing libraries needed for web scraping 
import requests
from bs4 import BeautifulSoup

# Imports for rendering the web app 
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash import dcc 

# Importing the app instance 
from app import app

# Importing functions for fetching data
from pages.funcs import fetch

# Import the LSTM algorithm 
from LSTM.LSTM import LSTMAlgorithm

# Importing the data management library to read CSV 
import pandas as pd

# Generate the search field 
text_input = html.Div(
    [
        html.Div(dbc.Input(id="input", placeholder="Ticker", type="text", debounce=True), style = {
            
        }),
        html.Br(),
        html.Div(id="output"),
    ]
)

# Read and store the watchlist from the JSON
with open("pages/watchlist.json") as jsonFile:
    currentWatchlist = json.load(jsonFile)['watchlistStocks']
    
    jsonFile.close()

# Read and store the portfolio from the JSON 
with open("pages/portfolioStocks.json") as jsonFile:
    currentPortfolio = json.load(jsonFile)['portfolioStocks']
    
    jsonFile.close()

# Split the layout into two variables for organization 
layout_output = html.Div(
    [html.Div(id = 'layout-output', style = {})],
    id = 'layout-content'
)

# Store the ticker names as a stack like format 
tickerName = []
# Decorater function to manage the layout based on the user search 
@app.callback(
    Output("layout-content", "children"), 
    [Input("input", "value")]
)
def output_text(value):
    """
    This function is used to generate the content for the page after a stock ticker name has been entered.
    Args:
        value: string
    Returns:
        if code runs properly:
            buttons: Div
            Div of returnChild
        otherwise: 
            dbc.Toast
    """
    # The try here is in case the fetcher does not find a stock with a matching ticker name that was inputted by the user. If so, it goes to the except.
    try: 
        # Getting information about the graph, fullname, details (open, high, low, etc) using the functions we created in fetch.py
        fig, fullname, info = fetch.searchData(str(value).upper())
        # Getting the graph of the future of the stock using machine learning
        predictionFigure = LSTMAlgorithm(str(value).upper())
        # Creating the dbc component showing the graph and information of the stock that will go into the page
        stockInfo = dbc.Row([
                # This is formatted using columns. One for the graph and another for the information.
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
        
        # Creating the add to watchlist and portfolio buttons
        buttons = html.Div(
            [
                # The buttons for adding to watchlist and portfolio
                dbc.Button("Watchlist +", color="warning", disabled=False, id='watchlist-add'),
                dbc.Button("Portfolio +", color="danger", disabled=False, id='portfolio-add'),
                # The modal popup where the user adds a stock to portfolio
                dbc.Modal(
                    [
                        # The parts of the modal
                        dbc.ModalHeader(dbc.ModalTitle("Add to Portfolio"), close_button=True),
                        dbc.ModalBody([
                            dbc.Input(id="volume-input", placeholder="Number of Shares Bought", type="text", debounce = True), 
                            dbc.Input(id="buy-date", placeholder="Date Bought (DD/MM/YYYY)", type="text", debounce = True),
                        ], id = "modalbody"),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Submit",
                                id="submit-button",
                                className="ms-auto",
                                n_clicks=0,
                            )
                        ),
                    ],
                    # Giving an id to the modal and formatting it. We also set it's default state to false.
                    id="portfolio-popup",
                    centered = True,
                    is_open = False,
                ),
            # The bootstrap styling (here, we used bootstrap instead of css since we wanted to learn it)
            ], className="d-grid gap-2 col-6 mx-auto"
        )
        # Putting the current stocks ticker into the stack where it will be used later for adding to portfolio and watchlist. We can easily retrieve the most recent ticker name searched because we're using a stack. We keep the old ticker names searched in case we wanted to implement a back system.
        tickerName.append(value.upper())
        # Returning the layout we created in this function (the buttons, the stock info, and the machine learning prediction).
        return [
            buttons, 
            html.Div(
                [stockInfo], 
                id='layout-output', 
                style = {'margin-top' : '30px'}
            ),
            html.Div(
                dcc.Graph(figure = predictionFigure)
            )]
    # If the user inputted an invalid stock name, then the except statement will return an error message.
    except: 
        if value is not None:
            # This is the error notification
            return [dbc.Toast(
                [html.P("Please enter a valid ticker that can be found on Yahoo Finance", className="mb-0")],
                id="auto-toast",
                header="Invalid Ticker",
                icon="danger",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]

# This callback toggles whether the portfolio-popup modal is open or not. It will toggle it whenever portfolio-add or submit-button is clicked
@app.callback(
    Output("portfolio-popup", "is_open"),
    [
        Input("portfolio-add", "n_clicks"), 
        Input("submit-button", "n_clicks")
    ],
    [State("portfolio-popup", "is_open")],
)
def toggle_modal(portfolioClicks, submitClicks, is_open):
    """
    Toggles whether the portfolio-popup modal is open or not 
    Args:
        portfolioClicks: int
        submitClicks: int
        is_open: bool
    Returns:
        not is_open: bool
    """
    # Toggle the state of modal's open variable if it has been clicked. 
    if portfolioClicks or submitClicks:
        return not is_open

# This callback was used to take the information for updating portfolio and outputting the success notification
@app.callback(
    Output('portfolio-toast', 'children'),
    [
        Input('submit-button', 'n_clicks'),
        Input('volume-input', 'value'),
        Input('buy-date', 'value')
    ]
)
def updatePortfolio(clicks, volumeValue, buyDate):
    """
    Updates portfolio when the user enters something into the portfolio popup
    Args:
        clicks: int
        volumeValue: str
        buyDate: str
    """
    # The program checks here to make sure that the user actually inputted
    if volumeValue is not None and buyDate is not None:
        # Try except for converting the volume to make sure its a valid number 
        try:
            # Convert the volume to float 
            volumeValue = float(volumeValue)
            # Take the date input and split it at the slashes 
            dates = str(buyDate).split('/')
            
            # There must be three elements in the dates list: year, month, and day 
            # Month and day must be 2 characters long and year must be 4 
            if len(dates) == 3 and len(dates[0]) == 2 and len(dates[1]) == 2 and len(dates[2]) == 4:
                try:
                    # Get the current UNIX time 
                    currentUnixTime = str(int(time.time()))

                    # Get the information from the dates list 
                    buyYear = int(dates[2])
                    buyMonth = int(dates[1])
                    buyDay = int(dates[0])

                    # Get the UNIX time for when the user bought the stocks 
                    pastUnixTime = time.mktime(datetime.date(buyYear, buyMonth, buyDay).timetuple()) 
                    
                    # Make sure that the past UNIX time is greater than the current UNIX time otherwise give the error toast
                    if int(pastUnixTime) > int(currentUnixTime):
                        return [dbc.Toast(
                            id="auto-toast",
                            icon="danger",
                            header=f"Invalid date input. Try Again.",
                            duration=2750,
                            is_open=True,
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                        )]
                    
                    # Try to get the price of the stock on the day it was bought 
                    try:
                        # Download CSV of that date 
                        historicalCSV = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{tickerName[-1]}?period1={int(pastUnixTime) - 86400}&period2={int(pastUnixTime)}&interval=1d&events=history&includeAdjustedClose=true')
                        
                        # Remove the buyPrice from the CSV 
                        buyPrice = int(historicalCSV.loc[0].at['Open'])

                    # Otherwise, give the error message since there is no stock data for that day
                    except:
                        return [dbc.Toast(
                            id="auto-toast",
                            icon="danger",
                            header=f"Date inputted cannot be a date when the market was closed.",
                            duration=2750,
                            is_open=True,
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                        )]
                    # This try except is used to check if industry data exists for the stock, and if it does to add it to the JSON
                    try: 
                        # URL to parse data from 
                        URL = f'https://finance.yahoo.com/quote/{tickerName[-1]}/'

                        # Scrape the page and get the HTML code 
                        page = requests.get(URL)
                        soup = BeautifulSoup(page.content, "html.parser")
                        
                        # Parse through the HTML to get the actual industry name 
                        industry = soup.find_all(class_='D(ib) Va(t)'); 
                        industry = industry[0] 
                        industry = str(industry).split(':')[2]; 
                        industry = industry.split('Fw(600)">')[1] 
                        industry = industry.split('<')[0]

                        # If the data is not already in portfolio, append it 
                        if [tickerName[-1], volumeValue, buyDate, buyPrice, industry] not in currentPortfolio:
                            currentPortfolio.append([tickerName[-1], volumeValue, buyDate, buyPrice, industry])
                        
                        # If the page is not loading right now, sort it alphabetically and dump it into the JSON
                        if clicks is not None:
                            currentPortfolio.sort(key = lambda x : x[0])
                            jsonData = {
                            "portfolioStocks" : currentPortfolio
                            }
                            with open('pages/portfolioStocks.json', 'w') as jsonFile:
                                json.dump(jsonData, jsonFile)
                                jsonFile.close()

                            # Show the success notification
                            return [dbc.Toast(
                                id="auto-toast",
                                icon="success",
                                header="Added to your portfolio",
                                duration=2750,
                                is_open=True,
                                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                            )]
                    
                    # This except occurs when the industry data does not exist 
                    except:
                        # Make sure that the data that we have is not already in the portfolio 
                        if [tickerName[-1], volumeValue, buyDate, buyPrice] not in currentPortfolio:
                            # Add it to portfolio 
                            currentPortfolio.append([tickerName[-1], volumeValue, buyDate, buyPrice])
                        
                        # Use a lambda function to sort it alphabetically 
                        currentPortfolio.sort(key = lambda x : x[0])

                        # Store the portfolio data in a dictionary 
                        jsonData = {
                            "portfolioStocks" : currentPortfolio
                        }

                        # Dump the data into a JSON 
                        with open('pages/portfolioStocks.json', 'w') as jsonFile:
                            json.dump(jsonData, jsonFile)
                            jsonFile.close()
                        
                        # Success notification
                        return [dbc.Toast(
                            id="auto-toast",
                            icon="success",
                            header="Added to your portfolio",
                            duration=2750,
                            is_open=True,
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                        )]
                
                # If there is a date exception, then the code will through Exception error. We then output the error message for invalid date. 
                except Exception:
                    return [dbc.Toast(
                        id="auto-toast",
                        icon="danger",
                        header=f"Invalid date input. Try Again.",
                        duration=2750,
                        is_open=True,
                        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    )]
            
            # If the date is invalid, output the following error toast
            else:
                return [dbc.Toast(
                    id="auto-toast",
                    icon="danger",
                    header=f"Invalid date input. Try Again.",
                    duration=2750,
                    is_open=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )]

        # Output the error toast if the volume is not valid 
        except:
            # Make sure that the callback is not fired on page load 
            if volumeValue is not None:
                return [dbc.Toast(
                        id="auto-toast",
                        icon="danger",
                        header=f"Invalid volume input. Try Again.",
                        duration=2750,
                        is_open=True,
                        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    )]
    

# Define the decorator function for the watchlist button to display a success toast. 
@app.callback(
    Output("watchlist-toast", 'children'),
    [Input('watchlist-add', 'n_clicks')]
)
def updateWatchlist(n):
    """
    Updates the watchlist when the user clicks the button
    Args:
        n: int
    Returns:
        dbc.Toast
    
    Written by Eric. 
    """
    # Make sure that the user has actually inputted something and the function is not getting fired at page load 
    if n is not None:
        with open("pages/watchlist.json") as jsonFile:
            currentWatchlist = json.load(jsonFile)['watchlistStocks']
    
            jsonFile.close()
        # Make sure the stock is not already in the watchlist 
        if tickerName[-1] not in currentWatchlist: 
            # Append it to the watchlist 
            currentWatchlist.append(tickerName[-1])
            # Sort the watchlist alphabetically using a lambda function 
            currentWatchlist.sort(key = lambda x : x[0])
            # Store it in a dictionary
            jsonData={
                "watchlistStocks": currentWatchlist
            }
            # Dump it into the file 
            with open('pages/watchlist.json', 'w') as jsonFile:
                json.dump(jsonData, jsonFile)
                jsonFile.close()
        # If the ticker is already in watchlist, return the error toast 
        else:
            return [dbc.Toast(
                    id="auto-toast",
                    icon="danger",
                    header=f"{tickerName[-1]} is already in your watchlist",
                    duration=2750,
                    is_open=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )]
        # Return the success toast if the ticker was added to watchlist 
        return [dbc.Toast(
                id="auto-toast",
                icon="success",
                header="Added to your watchlist",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]

# Define the layout for the page 
layout = html.Div(children=[
    # Wrap the content in the spinner so that when the content is loading (due to the machine learning upping the runtime), there will be a loading spinner. 
    dbc.Spinner(children = [dbc.Row([
        dbc.Col([]),
        dbc.Col([text_input]),
        dbc.Col([])
    ]),
    dbc.Row([dbc.Col([layout_output])])], type = "grow", color = "success"),
    html.Div(id = 'watchlist-toast'),
    html.Div(id = 'portfolio-toast')
], id='page-content')
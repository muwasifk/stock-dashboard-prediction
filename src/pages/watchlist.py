"""
ICS3U 
Muhammad Wasif Kamran 
This file contains the code to display the watchlist page. 
"""

# Import json library to access JSON file 
import json

# Import the libraries needed to render the website
from dash import html, Output, State, Input
import dash_bootstrap_components as dbc

# Import the functions needed to fetch the data 
from pages.funcs import fetch

# Import the app instance for callbacks 
from app import app

def formtable():
    """
    This function generates the content for the table. 
    Args: 
        None 
    Returns: 
        table: dbc.Table 
    """
    # Read the JSON file to get the tickers to display
    with open("pages/watchlist.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    # Store the tickers in an array
    watchlistStocks = jsonObject["watchlistStocks"]

    # Generate the table header with the different stats to be displayed 
    tableHeader = [
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

    # Create a rows list to contain the row components 
    rows = []

    # Iterate over the length of the list of tickers
    for i in range(0, len(watchlistStocks)):
        # From the fetch.py, get the data needed for this page
        curData = fetch.watchlistFetchData(watchlistStocks[i])
        # Generate a table row (Tr) and append it to the rows list  
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

    # Store the table body of rows in a list   
    tableBody = [html.Tbody(rows)]

    # Generate the table by combining the header and body with settings: table should not have a border, should be striped, and if mouse is hovering it changes color
    table = dbc.Table(tableHeader + tableBody, bordered = False, striped = True, hover=True)
    
    # Return the table component to be displayed in layout 
    return table

# Generate the layout and store it in a div 
layout = html.Div(children=[
    # Header text for the page 
    html.H1(
        children="WATCHLIST", # Text to be displayed
        style = {
            'text-align': 'center', # Center of page
            'color': '#4db6ac', # Setting color to green
            'font-family': 'Montserrat' # Changing font
        }
    ),
    # Div with the table 
    html.Div(
        style = {
            'margin': 'auto', # Automatically making margins as needed
            'width': '90%', # Changing width of table to 90% of full screen width
            'padding': '30px', # Adding 30px of padding on all sides 
            'text-align': 'center' # Align the text in the center of table
        },
        id = 'body-table' # Give the div an id 
    ),
    # Div with refresh and remove buttons 
    html.Div(
        # Row to contain the two buttons 
        dbc.Row([
            
            # Refresh button 
            dbc.Col(dbc.Button(
                children = 'Refresh Data',
                style = {
                    'text-align': 'center'
                },
                id='refresh-button',
                n_clicks=0,  outline=True, color="success"
            )),

            # Remove button
            dbc.Col(dbc.Button(
                children = 'Remove stock',
                style = {
                    'text-align': 'center'
                },
                id='remove-button',
                n_clicks=0,  outline=True, color="danger"
            ), width=6)
        ]), 
        # The styling for the div containing the buttons
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        }
    ), 
        # Modal for the remove stock option 
        dbc.Modal(
            [
                # Title of the input box 
                dbc.ModalHeader(dbc.ModalTitle("Remove a stock"), close_button=True),
                # Body of the modal
                dbc.ModalBody([
                    # Input field for the ticker 
                    dbc.Input(id="removed-stock", placeholder="Stock ticker (in caps)", type="text", debounce = True),
                ], id = "watchlist-remove-modal"),
                # Footer of the modal
                dbc.ModalFooter(
                    # Submit button
                    dbc.Button(
                        "Submit",
                        id="submit-button",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="remove-popup-watchlist",
            centered=True,
            is_open=False,
        ),
        # Toast notification
        html.Div(id = 'remove-toast2')
], id='page-content')

# Decorator function that takes the input from the refresh button and number of times clicked and outputs the table's children component
@app.callback(
    Output('body-table', 'children'),
    Input('refresh-button', 'n_clicks')
)
def refreshTable(n):
    """
    This function generates the table. 
    Args: 
        None 
    Returns: 
        [table]: list
    """
    # Generate the table 
    table = formtable()
    # Return it in a list as the children parameter of the body-table takes lists  
    return [table]

# Decorator function to manage the watchlist modals and exiting by taking the inputs as submit and 'x' button at the corner and returning the state of the modal open
@app.callback(
    Output('remove-popup-watchlist', 'is_open'),
    [Input('remove-button', 'n_clicks'),
    Input('submit-button', 'n_clicks')],
    [State('remove-popup-watchlist', 'is_open')]
)
def removePopup(removeClicks, submitClicks, is_open):
    """
    This function closes the popup when the user submits or closes the modal. 
    Args: 
        removeClicks: int
        submitClicks: int 
        is_open: bool
    Returns: 
        is_open: bool
    """
    # If the remove button or the submit button has been clicked, change the state of the modal to not open 
    if removeClicks or submitClicks:
        return not is_open

# Initialize last removed variable to hold the stock that has been removed most recently. 
lastRemoved = ""

# Decorator function to manage the removing of a stock from the watchlist by taking the number of times submit has been clicked and the value in the input field to determine which stock is to be removed and outputs a toast notification
@app.callback(
    Output('remove-toast2', 'children'),
    [
        Input('submit-button', 'n_clicks'),
        Input('removed-stock', 'value'),
    ]
)
def removeWatchlistStock(clicks, ticker):
    """
    This function removes a stock from the watchlist from user input and gives a confirmation notification.
    Args: 
        clicks: int 
        ticker: str 
    Returns: 
        [dbc.Toast]: list
    """
    # Make sure that the button has actually been clicked, otherwise the function will fire on page load 
    if clicks is not None: 
        # Open the JSON and store the data in list 
        with open("pages/watchlist.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        watchlistStocks = jsonObject["watchlistStocks"]
        
        # Error handling to make sure that the inputted ticker is actually in the list 
        try: 
            # This code runs if the ticker exists in list
            # Remove the ticker from the list 
            watchlistStocks.remove(ticker)

            # Create a dictionary with the updates list 
            jsonObject = {'watchlistStocks': watchlistStocks}
            # Open the JSON and dump the new information in 
            with open('pages/watchlist.json', 'w') as jsonFile: 
                json.dump(jsonObject, jsonFile)
                jsonFile.close()
            
            # Update the last removed ticker
            lastRemoved = ticker
            # Return a success toast notificiation 
            return [dbc.Toast(
                id="success-toast",
                icon="success",
                header=f"Success! Removed from your watchlist.",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]
        except:
            # This code runs if the ticker is not in list 
            # Making sure the user actually inputted a ticker and not empty and that they actually clicked the button as opposed to page load 
            # Make sure that the call back is not firing again unexpectedly (through the last removed condition)
            if ticker is not None and clicks is not None and lastRemoved != ticker: 
                # Return an error toast 
                return [dbc.Toast(
                id="error-toast",
                icon="danger",
                header=f"Invalid ticker name. Try Again.",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]
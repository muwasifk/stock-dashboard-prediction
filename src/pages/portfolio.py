"""
ICS3U 
Muhammad Wasif Kamran & Eric Sui
This file contains the code for the layout of the portfolio page. This file was considerably larger than the others and was thus a joint effort. Most of the code was written by Eric and the code written by Wasif is marked in the docstrings with "Written by Wasif."
"""
# Importing the needed libraries
import json
from dash import html, Output, Input, State, dcc
from pages.funcs import fetch
from app import app 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Setting the colors for the page
colors = {
    'background': '#111111',
    'text': '#363636'
}

def calculateValue():
    """
    Finds the total value of the portfolio
    Args:
        None
    Returns:
        total: int
    """
    # Open the json file
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    # Retrieve the portfolio's stocks form the json file
    portfolioStocks = jsonObject["portfolioStocks"]

    # Creating a variable for the total value
    total = 0

    # Add up all the values of the stocks in the portfolios
    for i in portfolioStocks:
        ticker = i[0]
        currentPrice = float(fetch.portfolioFetchData(ticker).replace(",",""))
        total += currentPrice * i[1]
    
    # Return the calulated value to 2 decimal places
    return round(total, 2)


def formtable():
    """
    This function creates a table that displays the portfolio
    Args:
        None
    Returns:
        table: html.Table
    """
    # Open the json file
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    # Retrieve the portfolio's stocks form the json file
    portfolioStocks = jsonObject["portfolioStocks"]
    
    # Begin creating the table
    table_header = [
        # The headers of the table columns
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

    # Variables that are used later for certain information
    totalProfit = 0
    totalBalance = 0

    # Making a list for the table rows
    rows=[]

    # This for loops generates each of the rows for each of the stocks in the portfolio
    for i in range(0, len(portfolioStocks)):
        # currentStock is the list of the stock information for the current row
        currentStock = portfolioStocks[i]
        # ticker is the ticker of the stock
        ticker = currentStock[0]
        # currentPrice is the current price of the stock that is found using the webscraper
        currentPrice = float(fetch.portfolioFetchData(ticker).replace(",",""))
        # buyPrice is the price of the stock when it was bought
        buyPrice = currentStock[3]
        # volume is the amount of shares bought
        volume = currentStock[1]
        # Calculating the profit and rounding to 2 decimals places
        profit = round((currentPrice - buyPrice) * volume, 2)
        # dateBought is the date the stock was bought
        dateBought = currentStock[2]
        # Adding the monetary value to the balance and profit
        totalBalance += currentPrice*volume
        totalProfit += profit

        # Now creating the row and appending it to the list
        rows.append(html.Tr([
            html.Td(ticker),
            html.Td(f"{currentPrice}$"),
            html.Td(f"{buyPrice}$"),
            html.Td(f"{volume}"),
            html.Td(f"{profit}$"),
            html.Td(dateBought)
        ]))

    # Creating the table body using the list of rows
    table_body = [html.Tbody(rows)]

    # Creating and returning the table by combining the header and body
    table = dbc.Table(table_header + table_body, striped = True, hover = True, id="tabletable")
    return table 

def formPieChartVolume():
    """
    This function creates a pie chart displaying information about the volumes of the stocks in portfolioStocks
    Args:
        None
    Returns:
        volumePieGraph: go.Figure
    
    Written by Wasif. 
    """
    # Opening the json file containing the portfolio info
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    portfolioStocks = jsonObject["portfolioStocks"]

    # Initializing lists for the lables and values of the stocks that will be used for the stock volume pie graph
    labels = []
    values = []

    # Putting information in the lists
    for i in range(0, len(portfolioStocks)):
        labels.append(portfolioStocks[i][0]) 
        values.append(portfolioStocks[i][1])

    # Creating and returning the pie graph
    volumePieGraph = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, title = 'Volume Composition')])
    return volumePieGraph 

def formPieChartValue():
    """
    This function creates a pie graph displaying information about the monetary values of the stocks in portfolioStocks
    Args:
        None
    Returns:
        valuePieGraph: go.Figure
    
    Written by Wasif. 
    """
    # Opening the json file
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    portfolioStocks = jsonObject["portfolioStocks"]

    # Initializing a list for the labels and values
    labels = []
    values = []

    # Putting information in the lists
    for i in range(0, len(portfolioStocks)):
        labels.append(portfolioStocks[i][0])
        value = int(float(fetch.portfolioFetchData(portfolioStocks[i][0]).replace(",",""))) * portfolioStocks[i][1]
        values.append(value)

    # Creating and returning the pie graph
    valuePieGraph = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, title = 'Value Composition')])
    return valuePieGraph 

def formbarchart():
    """
    This function creates a pie graph displaying information about the industries of the stocks in portfolioStocks
    Args:
        None
    Returns:
        industryBarGraph: go.Figure
    
    Written by Wasif. 
    """
    # Opening the json file
    with open("pages/portfolioStocks.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    portfolioStocks = jsonObject["portfolioStocks"]
    
    # Initializing a dictionary and two lists for the bar graph
    industryCounts = {}

    x = []; y = []

    # This for loops goes through portfolioStocks and puts the info about the industries into industryCounts
    for i in range(0, len(portfolioStocks)):
        # This if statement checks if the current stock info being added has an industry
        if len(portfolioStocks[i]) == 5:
            # The following code adds the industry info 
            if portfolioStocks[i][0] not in industryCounts.keys():
                industryCounts[portfolioStocks[i][4]] = portfolioStocks[i][1]
            else:
                industryCounts[portfolioStocks[i][4]] += portfolioStocks[i][1]
    # Appending the names of the industries and the volume for each industry to the x and y axes
    for i in industryCounts.keys():
        x.append(i); y.append(industryCounts[i])
    
    # Creating and returning the graph
    industryBarGraph = go.Figure([go.Bar(x=x, y=y)])

    # Return the figure
    return industryBarGraph

# Writing the layout for the page
layout = html.Div(children = [
    # Creating the heading for the page 
    html.H1(
        children = "YOUR PORTFOLIO",
        style = {
            'text-align': 'center',
            'color': '#4db6ac',
            'font-family': 'Montserrat'
        }
    ),
    # Creating a div for the value of the portfolio
    html.Div(
        children = [
            # Creating the headings for the text
            html.H3(
                children = "Current Value:",
                style= {
                    'text-align': 'left',
                    'font-family': 'Montserrat'
                }
            ),
            html.H1(
                children = "",
                style= {
                    'text-align': 'left',
                    'font-family': 'Montserrat'
                },
                id = 'number-value'
            )
        ],
        # Styling the div (mainly just positioning)
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        }
    ),

    # Creating a div for the two pie graphs
    html.Div(
        children = [
            # We organize the three graphs using rows and columns
            dbc.Row(
                [dbc.Col(
                    dcc.Graph(id = "volumepie"),
                    style = {
                        'margin-left' : '30px'
                    }
                ),
                 dbc.Col(
                        dcc.Graph(id = "industrybar", style = {'justify' : 'center'})
                    ),
                dbc.Col(
                    dcc.Graph(id = 'valuepie'),
                    style = {
                        'margin-right' : '30px'
                    }
                )]
            ),

        ],
        id = "piegraphs"
    ),
    
    # Creating a div where the table will go
    html.Div(
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        },
        id = 'body-table2'
    ),

    # Creating the refresh and remove stock buttons
    html.Div(
        # Organizing the two buttons using columns in a row
        children = [dbc.Row([
            # Creating the two buttons
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
        # The styling for the div containing the buttons
        style = {
            'margin': 'auto',
            'width': '90%',
            'padding': '30px',
            'text-align': 'center'
        }
    ),

    # The following element creates a modal (pop-up) that the user uses as an inteface to remove a stock
    dbc.Modal(
        # Creading the head, footer, and body of the portfolio add modal
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
        # The id and styling of the Modal
        id="remove-popup-portfolio",
        centered=True,
        is_open=False,
    ),
    # Creating an id where a toast (notifaction) will pop up
    html.Div(id = 'remove-toast')
])

#The callback for the remove and submit buttons on the portfolio remove modal (if the user clicks on one of these, the modal closes or opens)
@app.callback(
    Output('remove-popup-portfolio', 'is_open'),
    [Input('remove-button', 'n_clicks'),
    Input('submit-button', 'n_clicks')],
    [State('remove-popup-portfolio', 'is_open')]
)
def removePopup(removeClicks, submitClicks, is_open):
    """
    Toggles the remove stock modal
    Args:
        removeClicks: int
        submitClicks: int
        is_open: bool
    Returns:
        not is_open: bool
    """
    # If one of the click numbers are greater than 0 when the callback fires (this is necessary because all the callback)
    if removeClicks or submitClicks:
        return not is_open
    
# The callback for actually removing the stock from the portfolio and adding a toast that pops up saying that the stock has been removed
@app.callback(
    Output('remove-toast', 'children'),
    [
        Input('submit-button', 'n_clicks'),
        Input('removed-stock', 'value'),
        Input('removed-stock-volume', 'value')
    ]
)
# This function removes the stock from the portfolio
def removePortfolioStock(clicks, ticker, removedNum):
    """
    Removes the specified amount of the inputted stock from the portfolio
    Args:
        click: int
        ticker: str
        removedNum: float
    Returns:
        dbc.Toast 
    """
    # These if statements check that the user actually inputed a volume and that it's positive.
    if removedNum is not None:
        if int(removedNum) <= 0:
            # The following return statement returns a toast that is used as a notification to notify the user about the invalid input
            return [dbc.Toast(
                id="error-toast",
                icon="danger",
                header=f"Invalid ticker volume (negative input detected). Try Again.",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]
    
    # The try here is in case the program encounters any conversion errors when converting ticker to a string
    try:
        # Error handling in case the user doesn't input a value for ticker
        if ticker is not None:
            ticker = str(ticker)

            # Make sure the ticker is uppercase
            if ticker != ticker.upper():
                return [dbc.Toast(
                    id="error-toast",
                    icon="danger",
                    header=f"Ticker name must be in capitals.",
                    duration=2750,
                    is_open=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )]
            
            if ticker.isnumeric(): 
                return [dbc.Toast(
                    id="error-toast",
                    icon="danger",
                    header=f"Ticker name must be letters.",
                    duration=2750,
                    is_open=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )]
        # Checking that the user actually clicked the button 
        if clicks is not None:
            # Opening the json file and retrieving the data into a variable
            with open("pages/portfolioStocks.json") as jsonFile:
                jsonObject = json.load(jsonFile)
                jsonFile.close()
            portfolioStocks = jsonObject["portfolioStocks"]
            # Creating the new list of stocks for the portfolio
            newPortfolioStocks = []
            # Here, removedNum is divided by 2 since the callback is called twice
            removedNum /=2

            # The following while loop is used to go through the stocks 
            i=0
            while (i < len(portfolioStocks)):
                # The algorithm now checks if the current stock the loop is currently on has a matching ticker
                if portfolioStocks[i][0] != ticker:
                    # If it doesnt, the stock gets added to the new list which will be put into portfolioStocks
                    newPortfolioStocks.append(portfolioStocks[i])
                else:
                    # If the ticker matches, it first checks if removedNum > 0. If so, then it will remove some stocks
                    if removedNum > 0:
                        # If removedNum is greater than 0, it checks if the amount of stocks getting removed is greater than the volume of the stock in this list entry (there may be several list enteries in portfolioStocks for a single ticker)
                        if removedNum >= portfolioStocks[i][1]:
                            # If the if statement is true, then this entry will not get added to the new list and the volume in this entry is subtracted from removedNum. This continues until removedNum is no longer a positive integer or until all entries of portfolioStocks have been looped through.
                            removedNum -= portfolioStocks[i][1]
                        else:
                            # If removedNum is no longer greater than the volume of the next entry of the stock, then whats remaining of removedNum is subtracted from that entry and removedNum is set to 0. Thus, any future entries of the stock will be added to the new portfolio.
                            portfolioStocks[i][1] -= removedNum
                            removedNum = 0
                            # Whats remaining of the volume of this entry of the stock after subtraction is added to the new portfolio. Note that this will not be 0 since removedNum must be smaller than the current entry's volume to enter this if statement.
                            newPortfolioStocks.append(portfolioStocks[i])
                
                # This is simply to make the while loop go through all the entries in portfolioStocks
                i+=1

            # The program now checks if removedNum is greater than 0. This is to check that user actually has as many or more than the amount of stocks that they're trying to remove.
            if removedNum > 0:
                if ticker is not None:
                    # This returns an toast displaying an error message assuming ticker is not empty
                    return [dbc.Toast(
                        id="error-toast",
                        icon="danger",
                        header=f"Invalid ticker volume. Try Again.",
                        duration=2750,
                        is_open=True,
                        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    )]
                else:
                    # If ticker is empty then, this error should be shown
                    return [dbc.Toast(
                        id="error-toast",
                        icon="danger",
                        header=f"Invalid ticker. Try Again.",
                        duration=2750,
                        is_open=True,
                        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                    )] 
            
            else:
                # If the program reaches this point, then that means no errors have been found within the input. Thus, it will write the new portfolio information into the json file.
                jsonObject = {'portfolioStocks': newPortfolioStocks}
                with open('pages/portfolioStocks.json', 'w') as jsonFile:
                            json.dump(jsonObject, jsonFile)
                            jsonFile.close()
                # This returns a toast displaying a success message
                return [dbc.Toast(
                    id="success-toast",
                    icon="success",
                    header=f"Stock successfully removed",
                    duration=2750,
                    is_open=True,
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                )]
    # If the program finds an error, it will prompt invalid input.
    except:
        if removedNum is not None:
            return [dbc.Toast(
                id="error-toast",
                icon="danger",
                header=f"Invalid input. Try Again.",
                duration=2750,
                is_open=True,
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            )]

# These final callbacks are for the refresh button. When it's clicked, the table, pie graphs, and bar graph will be refreshed by calling their functions again and displaying them in the divs. Additionally, all the callbacks are fired once at the beginning of the program so this causes the elements to be displayed on the page without clicking the refresh button.
# The number refresh callback
@app.callback(
    Output("number-value", "children"),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshValue(n_clicks):
    """
    Refreshes the number displaying the value of the portfolio.
    Args:
        n_clicks: int
    Returns:
        portfolioValue: str
    """
    # The function checks if the user has clicked at least once. If so, they it creates a pie graph and returns it into the div.
    if n_clicks is not None: 
        portfolioValue = str(calculateValue())
        return portfolioValue

# The table refresh callback
@app.callback(
    Output('body-table2', 'children'),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshTable(n_clicks):
    """
    Refreshes the table for the portfolio.
    Args:
        n_clicks: int
    Returns:
        [table]: html.Table in a 1-element list
    """
    # The function checks if the user has clicked at least once. If so, they it creates a table and returns it into the div.
    if n_clicks is not None:
        table = formtable()
        return [table]

# The volume pie graph refresh callback
@app.callback(
    Output("volumepie", "figure"),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshVolumePie(n_clicks):
    """
    Refreshes the volume pie graph.
    Args:
        n_clicks: int
    Returns:
        fig: go.Figure
    
    Written by Wasif. 
    """
    # The function checks if the user has clicked at least once. If so, they it creates a pie graph and returns it into the div.
    if n_clicks is not None: 
        fig = formPieChartVolume()
        return fig

# The value pie graph refresh callback
@app.callback(
    Output("valuepie", "figure"),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshValuePie(n_clicks):
    """
    Refreshes the value pie graph.
    Args:
        n_clicks: int
    Returns:
        fig: go.Figure
    
    Written by Wasif. 
    """
    # The function checks if the user has clicked at least once. If so, they it creates a pie graph and returns it into the div.
    if n_clicks is not None: 
        fig = formPieChartValue()
        return fig

# The industry bar graph refresh callback
@app.callback(
    Output("industrybar", "figure"),
    [Input('refresh-button2', 'n_clicks')]
)
def refreshIndustryBar(n_clicks):
    """
    Refreshes the industry pie graph.
    Args:
        n_clicks: int
    Returns:
        fig: go.Figure
    
    Written by Wasif. 
    """
    # The function checks if the user has clicked at least once. If so, they it creates a bar graph and returns it into the div.
    if n_clicks is not None: 
        fig = formbarchart()
        return fig
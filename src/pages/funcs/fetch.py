"""
ICS3U 
Muhammad Wasif Kamran & Eric Sui
This file contains various functions that are used elsewhere in the project to webscrape data from Yahoo Finance. 
"""

# Import the Plotly libraries needed for core components and graphing
from dash import dcc
import plotly.graph_objects as go

# Import pandas to read CSV files into a DataTable and parse them easier
import pandas as pd
# Import time in order to get unix times for webscraping 
import time 

# Importing BeautifulSoup in order to parse the HTML data
from bs4 import BeautifulSoup
# Importing requests in order to download the HTML file from Yahoo Finance
import requests 

def currentPriceParser(soup):
    # Get the current price HTML snippet by finding div with name fin-streamer and class name Fw(b) Fz(36px) Mb(-4px) D(ib)
    currentPrice = soup.find_all('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")

    # Since find_all returns a list, take the 0th element 
    currentPrice = str(currentPrice[0])

    # The following algorithm searches through the string to find the number between the tags in an HTML snippet

    # lBool is a boolean to see if we have found the < character in the string
    # rBool is similar to lBool but for the > character
    lbool = False 
    gbool = True 
    currentPriceVal = ""
    # We iterate over the characters in currentPrice
    for i in currentPrice:
        # If the value of gBool is true and we have encountered a < character, set gBool to False since this is the initial < character for the HTML content and is expected to be index 0 in the string
        if gbool and i == "<": 
            gbool = False
            continue 
        # If lBool is false and we encountered the very first > character, set lBool to True and begin reading the current price in
        if i == ">" and not lbool: 
            lbool = True
            continue 
        # Whilst we are between the > character and the second < character, add the current value to currentPriceVal which maintains the current price
        if lbool == True and i != "<":
            currentPriceVal += i 
        # Once we hit the second < character, we are done reading the current price value and can exit the loop. 
        # We don't continune reading the string to optimize time complexity
        if i == "<" and not gbool: 
            break 
    
    # Yahoo Finance current market price data contains commas when the number is greater than 3 digits. Thus, we replace the commas with empty strings to be able to convert to float when needed
    currentPriceVal = currentPriceVal.replace(",", "")

    # Return the parsed value
    return currentPriceVal

def watchlistFetchData(ticker):
    """
    This function fetches data for the watchlist table using webscraping from Yahoo Finance 
    Args: 
        ticker: string 
    Returns: 
        [currentPriceVal, open, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow]: list
    """
    # Variable to hold the link to be webscraped 
    URL = f'https://finance.yahoo.com/quote/{ticker}'
    
    # Get the response code and data from Yahoo Finance
    page = requests.get(URL) 

    # Parse the data from the page
    soup = BeautifulSoup(page.content, "html.parser")

    # Call the parser function to get the value
    currentPriceVal = currentPriceParser(soup)

    # To get the stats table from Yahoo Finance, we search for the class name Ta(end) Fw(600) Lh(14px) with tags td 
    statsTable = soup.find_all('td', class_ = 'Ta(end) Fw(600) Lh(14px)')

    # The second element of the given statsTable will contain information about the open price for the stock 
    open = statsTable[1]
    # We first convert the data to a string and then splice from the 60th index to -5 to parse through the HTML code and get the actual value needed 
    open = str(open)[60:-5]

    # The fifth element of statsTable contains the day range which gives the lowest and highest value for the day in the format low - high
    dayRange = statsTable[4]
    # We convert the dayRange to string and splice to eliminate the HTML code
    dayRange = str(dayRange)[66:-5]
    # We split it at the - charater to further parse it
    dayRange = dayRange.split(" - ")
    # Since dayRange is now a list of two elements, we can simply read it into variables for convineience 
    low, high = dayRange[0], dayRange[1] 

    # For the 52 week range, we use a similar parsing method to the single day range 
    fiftyTwoWeekRange = statsTable[5] 
    fiftyTwoWeekRange = str(fiftyTwoWeekRange)[74:-5]
    fiftyTwoWeekRange = fiftyTwoWeekRange.split(" - ") 
    fiftyTwoWeekLow, fiftyTwoWeekHigh = fiftyTwoWeekRange[0], fiftyTwoWeekRange[1]
    
    # Add all the needed data to a list and return 
    return [currentPriceVal, open, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow]

def portfolioFetchData(ticker):
    """
    This function takes in a ticker and returns the current price of a stock to be used in the portfolio. While the code is similar to the watchlist code, it is better to compartmentalize and seperate the two in case we are going to be parsing other information in the future and need to add it to this function. 
    Args:
        ticker : string
    Returns:
        currentPriceVal : string
    """
    # Store the link that will be scraped using an fstring
    URL = f'https://finance.yahoo.com/quote/{ticker}/'

    # Get the HTML data from the URL and get the response code
    page = requests.get(URL) 
    # Parse the data into a readable format
    soup = BeautifulSoup(page.content, "html.parser")

    # Call the parser function to get the value
    currentPriceVal = currentPriceParser(soup)

    return currentPriceVal

def homePage(ticker):
    """
    This function returns the data needed for the home page. 
    Args: 
        ticker : string
    Returns:
        fig : plotly.graph_objects object
        [currentPriceVal, open, close, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow] : list
    """
    # We found out that Yahoo Finance generates its historical data CSV using a link that uses UNIX timestamps
    # We took the sample URL for a random stock and modified it as necessary 
    # The parts next to period1 and period2 are converting the current time to UNIX and subtracting 3 months worth of seconds and the latter being just the current time in UNIX
    df = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={int(time.time()-7689600)}&period2={int(time.time())}&interval=1d&events=history&includeAdjustedClose=true')

    # Generating the figure using the plotly.graph_objects library 
    # The first and only parameter is the data which contains the type of graph and the data where Data is on the x-axis and the candlesticks use open, high, low, and close numbers
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    
    # We store the value for the URL using an fstring to avoid concatenation
    URL = f'https://finance.yahoo.com/quote/{ticker}/'

    # Get the response code from the URL and HTML data
    page = requests.get(URL) 

    # Parse the data from the HTML file 
    soup = BeautifulSoup(page.content, "html.parser")

    # Call the parser function to get the value
    currentPriceVal = currentPriceParser(soup)

    # Get all the results from the HTML data with tag td and class name Ta(end) Fw(600) Lh(14px)
    statsTable = soup.find_all('td', class_ = 'Ta(end) Fw(600) Lh(14px)')
    
    # Open data is the data at index one in the stats table 
    open = statsTable[1]
    # Parse the data in the stats table  
    open = str(open)[60:-5]
    # Replace the commas with empty strings so that converting to float is possible 
    open = float(open.replace(',', ''))

    # Close data is the data at the 0th index in the stats table 
    close = statsTable[0]
    # Parse the data in the stats table
    close = str(close)[66:-5]
    # Replace the commas with empty strings so that converting to float is possible 
    close = float(close.replace(',', ''))
    
    # The day range is the data at index 4 in the stats table 
    dayRange = statsTable[4] 
    # Parse the data in the string
    dayRange = str(dayRange)[74:-5]
    # Split the string at the dash 
    dayRange = dayRange.split(" - ")
    # Replace the commas with empty strings so that converting to float is possible 
    low, high = float(dayRange[0].replace(',','')), float(dayRange[1].replace(',',''))

    # The 52W data is the data at the 4th index in the stats table 
    fiftyTwoWeekRange = statsTable[4]
    # Parse the data from the string in the stats table 
    fiftyTwoWeekRange = str(fiftyTwoWeekRange)[74:-5]
    # Split the string at the dash
    fiftyTwoWeekRange = fiftyTwoWeekRange.split(" - ") 
    # Replace the commas with empty strings so that converting to float is possible 
    fiftyTwoWeekLow, fiftyTwoWeekHigh = float(fiftyTwoWeekRange[0].replace(',','')), float(fiftyTwoWeekRange[1].replace(',',''))
    
    # Return the figure object along with a list of data used 
    return fig, [currentPriceVal, open, close, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow]

def searchData(ticker):
    """
    This function returns the data needed for the search page
    Args: 
        ticker : string
    Returns:
        dcc.Graph(figure=fig, config=config) : dash object 
        fullName : string
        [currentPriceVal, open, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow] : list
    """
    # Read the data from the CSV using UNIX timestamps 
    df = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{str(ticker).upper()}?period1={int(time.time()-7689600)}&period2={int(time.time())}&interval=1d&events=history&includeAdjustedClose=true')
    
    # For aesthetic purposes, make sure the mode bar on the graph is always displayed 
    config = {'displayModeBar': True}
    
    # Create the graph using the data from the CSV 
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    
    # Change the title of the graph and set the scale for the x axis
    fig.update_layout(title_text='Historical Stock Data', title_x = 0.5)
    
    # Store the URL to be scraped using fstrings to simplify concatenations 
    URL = f'https://finance.yahoo.com/quote/{ticker}/'

    # Get the error code and content from the URL
    page = requests.get(URL) 
    # Parse the data and store it as string
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the full name of the stock by finding class name D(ib) Fz(18px) and tag h1 
    fullName = soup.find_all('h1', class_='D(ib) Fz(18px)')
    # All results from previous statement are stored in list. Take first element and convert to string
    fullName = str(fullName[0])
    # Parse the HTML code out of the string
    fullName = fullName[27:-5]

    # Call the parser function to get the value
    currentPriceVal = currentPriceParser(soup)

    # Get all the results from the HTML data with tag td and class name Ta(end) Fw(600) Lh(14px)
    statsTable = soup.find_all('td', class_ = 'Ta(end) Fw(600) Lh(14px)')

    # Open data is the data at index one in the stats table 
    open = statsTable[1]
    # Parse the data in the stats table  
    open = str(open)[60:-5]
    # Replace the commas with empty strings so that converting to float is possible 
    open = float(open.replace(',', ''))

    # The day range is the data at index 4 in the stats table 
    dayRange = statsTable[4]; print (dayRange)
    # Parse the data in the string
    dayRange = str(dayRange)[66:-5]
    # Split the string at the dash 
    dayRange = dayRange.split(" - ")
    # Replace the commas with empty strings so that converting to float is possible 
    low, high = float(dayRange[0].replace(',','')), float(dayRange[1].replace(',',''))

    # The 52W data is the data at the 4th index in the stats table 
    fiftyTwoWeekRange = statsTable[5]
    # Parse the data from the string in the stats table 
    fiftyTwoWeekRange = str(fiftyTwoWeekRange)[74:-5]
    # Split the string at the dash
    fiftyTwoWeekRange = fiftyTwoWeekRange.split(" - ") 
    # Replace the commas with empty strings so that converting to float is possible 
    fiftyTwoWeekLow, fiftyTwoWeekHigh = float(fiftyTwoWeekRange[0].replace(',','')), float(fiftyTwoWeekRange[1].replace(',',''))

    # Return all the data needed for the search page that was webscraped  
    return dcc.Graph(figure=fig, config=config), fullName, [currentPriceVal, open, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow]


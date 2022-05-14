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

    # Find the current price of a stock by finding all elements with tag fin-streamer and class name Fw(b) Fz(36px) Mb(-4px) D(ib)
    currentPrice = soup.find_all('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")

    # Current price is originally a list, so we take the first element and convert it to a string
    currentPrice = str(currentPrice[0])

    # Declare a new variable since the value of currentPrice contains HTML fluff and needs to be parsed
    currentPriceVal = "" 

    # The following algorithm searches through the string to find the number between the tags in an HTML snippet

    # lBool is a boolean to see if we have found the < character in the string
    # rBool is similar to lBool but for the > character
    lBool = False 
    gBool = True 
    # We iterate over the characters in currentPrice
    for i in currentPrice:
        # If the value of gBool is true and we have encountered a < character, set gBool to False since this is the initial < character for the HTML content and is expected to be index 0 in the string
        if gBool and i == "<": 
            gBool = False
            continue 
        # If lBool is false and we encountered the very first > character, set lBool to True and begin reading the current price in
        if i == ">" and not lBool: 
            lBool = True
            continue 
        # Whilst we are between the > character and the second < character, add the current value to currentPriceVal which maintains the current price
        if lBool == True and i != "<":
            currentPriceVal += i 
        # Once we hit the second < character, we are done reading the current price value and can exit the loop. 
        # We don't continune reading the string to optimize time complexity
        if i == "<" and not lBool: 
            break 
    
    # Yahoo Finance current market price data contains commas when the number is greater than 3 digits. Thus, we replace the commas with empty strings to be able to convert to float when needed
    currentPriceVal.replace(",","")

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

    # Find the current price of a stock by finding all elements with tag fin-streamer and class name Fw(b) Fz(36px) Mb(-4px) D(ib)
    currentPrice = soup.find_all('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")

    # Current price is originally a list, so we take the first element and convert it to a string
    currentPrice = str(currentPrice[0])

    # Declare a new variable since the value of currentPrice contains HTML fluff and needs to be parsed
    currentPriceVal = "" 

    # The following algorithm searches through the string to find the number between the tags in an HTML snippet

    # lBool is a boolean to see if we have found the < character in the string
    # rBool is similar to lBool but for the > character
    lbool = False 
    gbool = True 
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
    currentPriceVal.replace(",","")
    # Return the parsed result
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
    
    # 
    URL = f'https://finance.yahoo.com/quote/{ticker}/'

    page = requests.get(URL) 
    soup = BeautifulSoup(page.content, "html.parser")

    currentPrice = soup.find_all('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")
    currentPrice = str(currentPrice[0])

    currentPriceVal = "" 
    lbool = False 
    gbool = True 
    for i in currentPrice:
        if gbool and i == "<": 
            gbool = False
            continue 
        if i == ">" and not lbool: 
            lbool = True
            continue 
        
        if lbool == True and i != "<":
            currentPriceVal += i 
        
        if i == "<" and not gbool: 
            break 
    
    currentPriceVal = currentPriceVal.replace(",","")

    statsTable = soup.find_all('td', class_ = 'Ta(end) Fw(600) Lh(14px)')
    
    open = statsTable[1]
    open = str(open)[60:-5]
    open = float(open.replace(',', ''))

    close = statsTable[0]
    close = str(close)[66:-5]
    close = float(close.replace(',', ''))
    
    dayRange = statsTable[4]; 
    dayRange = str(dayRange)[74:-5]
    dayRange = dayRange.split(" - ")
    low, high = float(dayRange[0].replace(',','')), float(dayRange[1].replace(',',''))

    fiftyTwoWeekRange = statsTable[4]
    fiftyTwoWeekRange = str(fiftyTwoWeekRange)[74:-5]
    fiftyTwoWeekRange = fiftyTwoWeekRange.split(" - ") 
    fiftyTwoWeekLow, fiftyTwoWeekHigh = float(fiftyTwoWeekRange[0].replace(',','')), float(fiftyTwoWeekRange[1].replace(',',''))
    
    return fig, [currentPriceVal, open, close, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow]

def searchData(ticker):
    df = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{str(ticker).upper()}?period1={int(time.time()-7689600)}&period2={int(time.time())}&interval=1d&events=history&includeAdjustedClose=true')
    config = {'displayModeBar': True}
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    
    fig.update_layout(title_text='Historical Stock Data', title_x = 0.5)
    
    URL = f'https://finance.yahoo.com/quote/{ticker}/'

    page = requests.get(URL) 
    soup = BeautifulSoup(page.content, "html.parser")

    fullName = soup.find_all('h1', class_='D(ib) Fz(18px)')
    fullName = str(fullName[0])
    fullName = fullName[27:-5]

    currentPrice = soup.find_all('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")
    currentPrice = str(currentPrice[0])

    currentPriceVal = "" 
    lbool = False 
    gbool = True 
    for i in currentPrice:
        if gbool and i == "<": 
            gbool = False
            continue 
        if i == ">" and not lbool: 
            lbool = True
            continue 
        
        if lbool == True and i != "<":
            currentPriceVal += i 
        
        if i == "<" and not gbool: 
            break 
    
    currentPriceVal.replace(",","")

    statsTable = soup.find_all('td', class_ = 'Ta(end) Fw(600) Lh(14px)')

    open = statsTable[1]
    open = str(open)[60:-5]

    dayRange = statsTable[4]; 
    dayRange = str(dayRange)[66:-5]
    dayRange = dayRange.split(" - ")
    low, high = dayRange[0], dayRange[1] 

    fiftyTwoWeekRange = statsTable[5] 
    fiftyTwoWeekRange = str(fiftyTwoWeekRange)[74:-5]
    fiftyTwoWeekRange = fiftyTwoWeekRange.split(" - ") 
    fiftyTwoWeekLow, fiftyTwoWeekHigh = fiftyTwoWeekRange[0], fiftyTwoWeekRange[1]

    return dcc.Graph(figure=fig, config=config), fullName, [currentPriceVal, open, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow]


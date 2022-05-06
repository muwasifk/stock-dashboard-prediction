from threading import currentThread
import requests
from bs4 import BeautifulSoup

def watchlistFetchData(ticker):
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
    
    return [currentPriceVal, open, high, low, fiftyTwoWeekHigh, fiftyTwoWeekLow]

def portfolioFetchData(ticker):
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

    currentPriceVal.replace(",","")
    return currentPriceVal


watchlistFetchData('TSLA')
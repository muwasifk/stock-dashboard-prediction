"""
ICS3U
Muhammad Wasif Kamran & Eric Sui 
This file contains the necessary code for the machine learning component of the project. 

NOTE: This code is heavily inspired from the tutorial https://towardsdatascience.com/time-series-forecasting-with-recurrent-neural-networks-74674e289816
"""

# Note that most of the numbers used here are found through trial and error until a realistic and somewhat accurate prediction was found for the testing set. The mathematical calculations to find the optimal values are too out of the scope of this course. 

# Import libraries for reading and managing data 
import pandas as pd
import numpy as np

# Import libraries for machine laerning algorithms 
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import LSTM, Dense

# Import libraries for graphing
import plotly.graph_objects as go

# Import libraries to getting up to date info
import time 

def predict(numPrediction, model, closeData, lookBack):
    """
    This function predicts the next values for 14 days (numPrediction = 14). 
    Args: 
        numPrediction: int 
        model: keras.model 
        closeData: list
        lookBack: int 
    Returns: 
        predictionList: list 
    """
    # Initialize the prediction list from before the look back value 
    predictionList = closeData[-lookBack:]
    
    # Iterate over the number of days to predict 
    for _ in range(numPrediction):
        # Let x be the portion of the prediction list to be considered from the look back days 
        x = predictionList[-lookBack:]
        # Reshape into the correct dimensions 
        x = x.reshape((1, lookBack, 1))
        # Output is the model's prediction 
        out = model.predict(x)[0][0]
        # Append the output to the prediction list 
        predictionList = np.append(predictionList, out)
    # Splice prediction list to go from the intial lookback value to the latest prediction 
    predictionList = predictionList[lookBack-1:]
    
    # Return the list of predictions 
    return predictionList
    
def predictDates(numPrediction, df):
    """
    This function is used to create a list of the dates that the data is predicted for. 
    Args: 
        numPrediction: int 
        df: pandas dataframe 
    Returns: 
        predictionDates: list 
    """
    # The intial date for the prediction is the one from the date 
    lastDate = df['Date'].values[-1]
    # The prediction dates are computed by making a date range from the last date of the training set to the number of dates to predicts and then coverting to a list. 
    predictionDates = pd.date_range(lastDate, periods=numPrediction+1).tolist()
    # Return a list of the dates that were predicted
    return predictionDates


def LSTMAlgorithm(ticker):
    """
    This function contains the code for the Long Short Term Memory Algorithm. 
    Args: 
        ticker: str
    Returns: 
        fig: go.Figure
    """

    # Get the current time in UNIX
    currentUnixTime = int(time.time())

    # Read the historical data from Yahoo finance with the unix timestamps with a difference of 2Y. 
    df = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={currentUnixTime - 63072000}&period2={currentUnixTime}&interval=1d&events=history&includeAdjustedClose=true')

    # Convert the values in date column to datetime objects for easier use. 
    df['Date'] = pd.to_datetime(df['Date'])
    #df.set_axis(df['Date'], inplace=True)
    # Remove the colomns for the open, high, low, and volume because they are not needed. 
    df.drop(columns=['Open', 'High', 'Low', 'Volume'], inplace=True)

    # Read the close values into a list 
    closeData = df['Close'].values

    # Reshape just in case so that the list has only one row. 
    closeData = closeData.reshape((-1,1))

    # Read the date values into a list 
    dateData = df['Date'].values

    # Split the previous data in 80% for training and 20% for testing 
    splitPercent = 0.80
    # Calculate the index at which to split the lists. 
    split = int(splitPercent*len(closeData))

    # Split the close data list to form the training and test lists 
    closeTrain = closeData[:split]
    closeTest = closeData[split:]

    # Numbers of days in the past used to forecast the next price.  
    lookBack = 15

    # Time series are data sets that track samples over time and allow one to see the factors influencing certain data over time. 
    # Generate batches of data from the training and test data while using the 15 day look back. The batch_size represents the number of samples that will be proccessed through the network before being assigned a weight (or importance for the prediction) 
    trainGenerator = TimeseriesGenerator(closeTrain, closeTrain, length=lookBack, batch_size=20)     
    testGenerator = TimeseriesGenerator(closeTest, closeTest, length=lookBack, batch_size=1)

    # Create a neural network called model 
    model = Sequential()
    # To the network add the Long Short Term Memory layer. The first parameter essentially represents the number of neurons in the model or the dimensions of the output. the ReLU activation is so that the output is either always positive or zero but never negative since stock prices cannot be negative. 
    model.add(LSTM(10, activation='relu'))
    # Add a dense layer which is basically the layer that takes in inputs and outputs the forecasting 
    model.add(Dense(1))
    # Compile the model using the adam optimizer and mean square error to manage data loss. These algorithms use complex mathematics and is the reason why the library is used. 
    model.compile(optimizer='adam', loss='mse')

    # Train the network using the training timeseries generator with 200 passes through the set to maximize accuracy without slowing the program down too much. 
    model.fit_generator(trainGenerator, epochs=200, verbose=1)

    # Predict the data for the test set for comparison. 
    prediction = model.predict_generator(testGenerator)

    # Reshape the lists to make sure they are one dimensional lists 
    closeTrain = closeTrain.reshape((-1))
    closeTest = closeTest.reshape((-1))
    prediction = prediction.reshape((-1))
    closeData = closeData.reshape((-1))

    # Create the layout for the graph 
    layout = go.Layout(
        title = "Prediction",
        xaxis = {'title' : "Date"},
        yaxis = {'title' : "Close"}
    )

    # Get the list of the forecast data
    forecast = predict(14, model, closeData, lookBack)
    # Get the list of the forecast dates 
    forecastDates = predictDates(14, df)

    # Make a scatter plot of the forecast values and dates
    trace1 = go.Scatter(
        x = forecastDates,
        y = forecast,
        mode='lines',
        name = 'Forecast'
    )

    # Make a scatter plot of the training and test values and dates 
    trace2 = go.Scatter(
        x = dateData,
        y = closeData,
        mode='lines',
        name = 'Previous'
    )

    # Generate the figure to display them together
    fig = go.Figure(data=[trace2, trace1], layout=layout)


    # Return the figure 
    return fig 



# Stock Dashboard and Predictor
This project contains a custom web based dashboard for stocks as well as machine learning algorithms to predict the prices of various stocks. 

>FOR THE GRADER: Inside the code, the files that were written by a specific person has their name in the header comments. 

<p align="center">
  <img src="https://img.shields.io/github/stars/wos-if/Stock-Dashboard-Prediction"/>
  <img src = "https://img.shields.io/github/forks/wos-if/Stock-Dashboard-Prediction" />
  <img src = "https://img.shields.io/github/issues/wos-if/Stock-Dashboard-Prediction" />
</p>

## Features 
- Watchlist & Portfolio
- Prominent Exchanges at a Glance
- Search Page to Find Information About Any Given Stock 
- Machine Learning Algorithm to Predict Prices of Stocks 

## Installation 
Make sure you are using Python 3.8.x in order for TensorFlow to work. 

Clone the repository 
```
git clone https://github.com/wos-if/Stock-Dashboard-Prediction
```
Install the dependencies 
```python
pip install -r requirements.txt
```

## Usage 
Run
```
cd src
python main.py 
```
In the terminal there will be a localhost link (most likely http://127.0.0.1:8000/) which you can enter into a browser (preferably Chromium based) to access the web app. The library used for rendering the web app will print out useless information in the console and it can be safely ignored. 
## Known Bugs
- The machine learning occasionally glitches out and gives an extremely unrelated result. Easiest way to fix is by refreshing the page. 
- When selling shares from the portfolio, entering lowercase values will bug it out and remove random amounts. 
- When the portfolio is empty, there is blank space rather than a blank pie chart. 
- The error handling for portfolio is a bit finicky. 

### Notes 
- When searching for a ticker, you may have to wait some time depending on your machine for the machine learning algorithm to run. 
- Upon launching the program, it may take time for the web app to actually load. 


## Support 
Email mkamr4@ocdsb.ca and esui1@ocdsb.ca or open an Issue/Pull Request

## Sources

### Sites / videos accessed for learning concepts
| Site / video                                                                                              | Purpose                                                                                                                                    |
|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| A Gentle Introduction to Long Short-Term Memory Networks by the Experts (machinelearningmastery.com)      | Learning about the general idea behind LSTM networks.                                                                                      |
| https://www.youtube.com/watch?v=b61DPVFX03I                                                               | To get an introduction for the machine learning and the algorithm                                                                          |
| https://realpython.com/beautiful-soup-web-scraper-python/                                                 | Learning how to webscrape code (used for getting data from Yahoo Finance).                                                                 |
| https://www.tensorflow.org/api_docs                                                                       | Docs for tensorflow, used for installing and using the machine learning                                                                    |
| https://keras.io/api/layers/recurrent_layers/lstm/                                                        | Keras docs to understand LSTM layer parameters.                                                                                            |
| https://www.youtube.com/watch?v=QciIcRxJvsM                                                               | Video used initially to gain insight as to how machine learning can be used for time series.                                               |
| https://dash.plotly.com/advanced-callbacks                                                                | Learning how callbacks in dash work to make live changes on the website and for interactivity                                              |
| https://dash.plotly.com/dash-core-components                                                              | Learning how the dash core components library works for basic templates for the layout                                                     |
| https://dash.plotly.com/dash-html-components                                                              | Learning how the dash html components library works for html templates for the layouts                                                     |
| https://dash-bootstrap-components.opensource.faculty.ai/                                                  | Learning how the dash bootstrap components works for certain components and templates for the layouts, such as rows, columns, and toasts.  |
| https://towardsdatascience.com/beginners-guide-to-building-a-multi-page-dashboard-using-dash-5d06dbfc7599 | Learning how to build a multi-page app in dash using an index file and apps folder with layouts.                                           |

### Code used from sites / videos
| Site / video                                                                                        | Code used / why                                                                                                                                                                        |
|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| https://towardsdatascience.com/time-series-forecasting-with-recurrent-neural-networks-74674e289816  | How to use the libraries and functions for the machine learning algorithm because the algorithm is quite complex and we did not know much about machine learning before this project.  |
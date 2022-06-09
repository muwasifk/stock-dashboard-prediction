"""
ICS3U 
Muhammad Wasif Kamran
This file stores the configuration code for the app. 
"""

# Import the libraries used to generate the website along with bootstrap components
import dash
import dash_bootstrap_components as dbc

# App contains the instance of the website and uses the FLATLY theme and Montserrat font
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY, 'https://fonts.googleapis.com/css?family=Montserrat'])
app.config.suppress_callback_exceptions = True 
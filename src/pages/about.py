import json
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.express as px

colors = {
    'background': '#111111',
    'text': '#363636'
}

layout = html.Div([
    html.H1(
        children = "About Us",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.H3(
        children = "This Project",
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'margin-left': '50px',
            'margin-right': '50px'
        }
    ),
    html.P(
        children = "This project was made by two grade 10 students at Merivale High School for their ICS3U project. This website provides data on various stocks and predicts their future prices using machine learning algorithms. Additionally, a portfolio and watchlist have been added for extra functionality. We hope you enjoy this website that we created. UwU",
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'margin-left': '50px',
            'margin-right': '50px'
        }
    ),
    html.H3(
        children = "Meet the Team",
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'margin-left': '50px',
            'margin-right': '50px'
        }
    ),
    html.P(
        children = "This project was created by Eric Sui and Muhammad Wasif Kamran. They're grade 10 students at Merivale High School. They both enjoy mathematics and computer science",
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'margin-left': '50px',
            'margin-right': '50px'
        }
    )]
)

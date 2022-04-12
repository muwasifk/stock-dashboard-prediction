import json
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import plotly.express as px

layout = html.Div(children=[
    html.H1(children="This is the watchlist page"),
], id='page-content')
import json

import dash
from dash import Input, Output, State, html, dcc

import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd

from pages import about, portfolio, watchlist, home, search

import plotly.graph_objs as go 

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY, 'https://fonts.googleapis.com/css?family=Montserrat'])

nav_item = dbc.NavItem(dbc.NavLink("Home", href="/home"))

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("About", href="/about"),
        dbc.DropdownMenuItem("My Portfolio", href="/portfolio"),
        dbc.DropdownMenuItem("My Watchlist", href="/watchlist"),
        dbc.DropdownMenuItem("Search", href="/search")
    ],
    nav=True,
    in_navbar=True,
    label="Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Machine Learning Stock Database"),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, dropdown], className="ms-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    className="mb-5"
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def displayPage(newpath):
    if newpath == '/about':
        return about.layout
    elif newpath == '/portfolio':
        return portfolio.layout
    elif newpath == '/watchlist':
        return watchlist.layout
    elif newpath == '/search':
        return search.layout
    else:
        return home.layout

if __name__ == "__main__":
    app.run_server(debug=False, port=8000)
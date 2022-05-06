import dash_bootstrap_components as dbc
from dash import html, Output, State, Input, dcc
from app import app

layout = html.Div(children=[
    html.Button("Holy shit its a button", id="body-button", n_clicks=0),
    html.Div(id="page-body")
], id = 'page-body')

@app.callback(
    Output("page-body", "children"), 
    Input("body-button", "n_clicks")
)
def showBody(n_clicks):
    return (f"Wow u clicked the button {n_clicks} times")
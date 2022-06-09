"""
ICS3U
Eric Sui
This file contains the code for global layouts and components that are meant to be displayed on every page (ie. navbar). 
"""

# Import the libraries needed to render the web app
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

# Import the various python files that contain the layouts
from pages import about, portfolio, watchlist, home, search

# Import the app instance for callbacks
from app import app

# Create an item on the navbar for the Home button which brings the user back to the main page
nav_item = dbc.NavItem(dbc.NavLink("Home", href="/home"))

# Create a dropdown component to access the other pages
dropdown = dbc.DropdownMenu(
    # Pages included in the dropdown
    children=[
        # About page with link being localhost/about
        dbc.DropdownMenuItem("About", href="/about"),
        # Portfolio page with link being localhost/portfolio
        dbc.DropdownMenuItem("My Portfolio", href="/portfolio"),
        # Watchlist page with link being localhost/watchlist
        dbc.DropdownMenuItem("My Watchlist", href="/watchlist"),
        # Search page with link being localhost/search
        dbc.DropdownMenuItem("Search", href="/search")
    ],
    # Enable the navbar
    nav=True,
    in_navbar=True,
    # The dropdown is called "Explore"
    label="Explore",
)

# Component for the actual navbar
navbar = dbc.Navbar(
    # Put into a container for CSS customizability
    dbc.Container(
        [
            # Name of the project at the top left
            dbc.NavbarBrand("Machine Learning Stock Database"),
            # Needed for callbacks to identify whether the navbar is being clicked on
            dbc.NavbarToggler(id="navbar-toggler"),
            # Collapse or expand the dropdown
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, dropdown], className="ms-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    # Bootstrap class for the container
    className="mb-5"
)


def toggle_navbar_collapse(n, is_open):
    """
    This function toggles the boolean for whether the navbar is open. 
    Args: 
        n: int
    Returns: 
        is_open: bool 
    """
    # n is the number of times the navbar has been clicked; if it is not 0, the navbar is not open
    if n:
        return not is_open
    return is_open


app.callback(
    Output(f"navbar-collapse", "is_open"),
    [Input(f"navbar-toggler", "n_clicks")],
    [State(f"navbar-collapse", "is_open")],
)(toggle_navbar_collapse)

# Define the basic layout for the webpage in a div
app.layout = html.Div([
    # Define the base url of the web app
    dcc.Location(id='url', refresh=False),
    # Display the navbar
    navbar,
    # Display the div with id page-content
    html.Div(id='page-content')
])

# Decorator callback which takes in the base url and desires pathname as inputs and returns the content of the page using the pathname
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])

def displayPage(newpath):
    """
    This function returns the content of the desired page.
    Args:
        newpath: string
    Returns: 
        layout: content of page in HTML div component 
    """
    # Returns the layout variable from the other files depending on the url
    # If none of the specific pages are selected, it displays the home page layout
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


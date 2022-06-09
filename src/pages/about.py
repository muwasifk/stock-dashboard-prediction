"""
ICS3U 
Eric Sui
This file contains the code for the about page.
"""

# Import necessary libraries for the layout
from dash import html

# Define the colors used in a dictionary
colors = {
    'background': '#111111',
    'text': '#363636'
}

# Variable which contains the layout of the page in a div
layout = html.Div(
    [
        # Header 1 
        html.H1(
            # Title text
            children = "About Us",
            # Style for the content: the text is aligned in the center and the color is from the dictionary above 
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        # Header 3
        html.H3(
            # Subtitle text
            children = "This Project",
            # Style for the content: text is aligned in the center, color is from the dictionary, the margins on left and right at both 50px
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'margin-left': '50px',
                'margin-right': '50px'
            }
        ),
        # Paragraph
        html.P(
            # Paragraph text
            children = "This project was made by two grade 10 students at Merivale High School for their ICS3U project. This website provides data on various stocks and predicts their future prices using machine learning algorithms. Additionally, a portfolio and watchlist have been added for extra functionality. We hope you enjoy this website that we created.",
            # Style for the content: text is aligned to the left, color is from dictionary, margins on left and right are both 50px 
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'margin-left': '50px',
                'margin-right': '50px'
            }
        ),
        # Header 3
        html.H3(
            # Subtitle text
            children = "Meet the Team",
            # Style for the content: aligned to the left, color is from dictionary, margins on left and right are 50px 
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'margin-left': '50px',
                'margin-right': '50px'
            }
        ),
        # Paragraph
        html.P(
            # Paragraph text
            children = "This project was created by Eric Sui and Muhammad Wasif Kamran. They're grade 10 students at Merivale High School. They both enjoy mathematics and computer science.",
            # Style for the content: text is aligned to the left, color is from dictionary, margins on left and right are 50px 
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'margin-left': '50px',
                'margin-right': '50px'
            }
        )
    ]
)

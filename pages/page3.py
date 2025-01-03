import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

# Initialize the Dash app with bootstrap theme
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data
box_score_data = {
    'Metric': ['Minutes', 'Points', 'Off. Rebounds', 'Def. Rebounds', 'Rebounds', 'Assists', 'Turnovers', 'Steals', 'Blocks'],
    'PER_GAME': [21.4, 9.8, 0.3, 2.5, 2.8, 2.2, 0.7, 0.8, 0.2],
    'PER_40_MINS': [40.0, 18.4, 0.6, 4.7, 5.3, 4.2, 1.2, 1.6, 0.5]
}

advanced_stats_data = {
    'Metric': ['Usage', 'Game Score', 'Off. Rating', 'Def. Rating', 'Off. Box +/-', 'Def. Box +/-', 'Box +/-', 'PORPAG', 'DPORPAG'],
    'Value': [15.7, 8.9, 146.3, 95.5, 5.8, 4.9, 10.7, 3.7, 2.8]
}

# Function to determine background color based on value
def get_background_color(value, column):
    if column in ['PER_GAME', 'Value']:
        if value > 10:
            return 'rgb(59, 130, 246)'  # Blue
        elif value > 5:
            return 'rgb(147, 197, 253)'  # Light blue
        elif value > 2:
            return 'rgb(252, 165, 165)'  # Light red
        else:
            return 'rgb(239, 68, 68)'    # Red
    return ''

# Create the layout
layout = dbc.Container([

    html.Div([
        html.A('Volver a la Página Principal', href='/')
    ]),


    dbc.Row([
        dbc.Col([
            html.H4("Box Score Statistics", className="text-center my-4"),
            dbc.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Metric"),
                        html.Th("PER GAME"),
                        html.Th("PER 40 MINS")
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(row['Metric']),
                        html.Td(f"{row['PER_GAME']:.1f}", style={'backgroundColor': get_background_color(row['PER_GAME'], 'PER_GAME')}),
                        html.Td(f"{row['PER_40_MINS']:.1f}")
                    ]) for _, row in pd.DataFrame(box_score_data).iterrows()
                ])
            ], bordered=True, hover=True)
        ], md=6),
        
        dbc.Col([
            html.H4("Advanced Statistics", className="text-center my-4"),
            dbc.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Metric"),
                        html.Th("Value")
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td(row['Metric']),
                        html.Td(f"{row['Value']:.1f}", style={'backgroundColor': get_background_color(row['Value'], 'Value')})
                    ]) for _, row in pd.DataFrame(advanced_stats_data).iterrows()
                ])
            ], bordered=True, hover=True)
        ], md=6)
    ])
], fluid=True)


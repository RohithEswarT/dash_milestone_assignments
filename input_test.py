import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = html.Div([
    html.P("User Input", className="text-primary", style={'float': 'left', 'color': 'black'}),
    html.P("Calculated Output", className="text-primary", style={'text-align': 'center', 'color': 'black'}),
    
    
    dbc.Row([
        dbc.Col([
            html.Label("Latitude", style={'margin-right': '10px'}),
            dcc.Input(id='latitude', type='number', value='', style={'width': '100%', 'color': 'black'}, placeholder="Latitude Eg: 39.6491"),
        ], md=6, className="mb-3"),
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Longitude", style={'margin-right': '10px'}),
            dcc.Input(id='longitude', type='number', value='', style={'width': '100%', 'color': 'black'}, placeholder="Longitude Eg: 79.922"),
        ], md=6, className="mb-3"),
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Data", style={'margin-right': '10px'}),
            dcc.Input(id='data', type='text', value='', style={'width': '100%', 'color': 'black'}, placeholder="Enter dataset GDP vs (country or year)"),
        ], md=6, className="mb-3"),
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Country", style={'margin-right': '10px'}),
            dcc.Input(id='country', type='text', value='', style={'width': '100%', 'color': 'black'}, placeholder="Enter a country name"),
        ], md=6, className="mb-3"),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button('Simulate', id='simulate-button', n_clicks=0, color="primary", className="mt-3"),
        ], md=6),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)

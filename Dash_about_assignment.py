import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
from dash_table import DataTable
import base64
import json

# Load Gapminder dataset
data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')



# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load config_about JSON file
with open('config_about.json', 'r') as f:
    config_about = json.load(f)
    summary_text = config_about['intro_part1']
    l1=config_about['intro_part1_list1']
    l2=config_about['intro_part1_list2']
    l3=config_about['intro_part1_list3']
    l4=config_about['intro_part1_list4']


# Define the layout
app.layout = html.Div([
    html.H1("Introduction to GapMinder", className="text-primary"),
    html.P(summary_text),
    html.P(l1),
    html.P(l2),
    html.P(l3),
    html.P(l4),
    
    # Filterable Table
    dbc.Row([
        dbc.Col([
            # Country Dropdown
            html.Label("Country"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in data['country'].unique()],
                multi=True
            )
        ], md=3),
        
        dbc.Col([
            # Continent Dropdown
            html.Label("Continent"),
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': continent, 'value': continent} for continent in data['continent'].unique()],
                multi=True
            )
        ], md=3),
        
        dbc.Col([
            # Population Range Slider
            html.Label("Population Range"),
            dcc.RangeSlider(
                id='pop-slider',
                min=data['pop'].min(),
                max=data['pop'].max(),
                step=100000,
                marks={i: str(i) for i in range(int(data['pop'].min()), int(data['pop'].max()), 200000000)},
                value=[data['pop'].min(), data['pop'].max()]
            )
        ], md=3),
        
        dbc.Col([
            # Life Expectancy Range Slider
            html.Label("Life Expectancy Range"),
            dcc.RangeSlider(
                id='lifeExp-slider',
                min=data['lifeExp'].min(),
                max=data['lifeExp'].max(),
                step=1,
                marks={i: str(i) for i in range(int(data['lifeExp'].min()), int(data['lifeExp'].max()), 10)},
                value=[data['lifeExp'].min(), data['lifeExp'].max()]
            )
        ], md=3)
    ], className="mb-3"),
    
    # Number of Rows Dropdown
    html.Label("Number of Rows Displayed"),
    dcc.Dropdown(
        id='rows-dropdown',
        options=[
            {'label': '5', 'value': 5},
            {'label': '10', 'value': 10},
            {'label': '20', 'value': 20},
            {'label': '50', 'value': 50}
        ],
        value=10
    ),
    
    # Download Button
    dbc.Button("Download Filtered CSV", id='download-button', color="success", className="mb-3"),
    
    # Download Link
    dcc.Download(id="download-data"),
    
    # Filtered Table
    html.Div(id='table-container')
])

# Callback to update filtered table
@app.callback(
    Output('table-container', 'children'),
    [Input('country-dropdown', 'value'),
     Input('continent-dropdown', 'value'),
     Input('pop-slider', 'value'),
     Input('lifeExp-slider', 'value'),
     Input('rows-dropdown', 'value')]
)
def update_table(country, continent, pop_range, life_exp_range, rows):
    # Filter the data based on user input
    filtered_data = data[(data['country'].isin(country) if country else True) &
                         (data['continent'].isin(continent) if continent else True) &
                         (data['pop'].between(pop_range[0], pop_range[1])) &
                         (data['lifeExp'].between(life_exp_range[0], life_exp_range[1]))]
    
    # Limit the displayed rows
    filtered_data = filtered_data.head(rows)
    
    # Generate DataTable
    table = DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in filtered_data.columns],
        data=filtered_data.to_dict('records'),
        style_table={'overflowX': 'scroll'}
    )
    
    return table

# Callback to download filtered data
@app.callback(
    Output("download-data", "data"),
    [Input('download-button', 'n_clicks')],
    [Input('country-dropdown', 'value'),
     Input('continent-dropdown', 'value'),
     Input('pop-slider', 'value'),
     Input('lifeExp-slider', 'value')]
)
def download_data(n_clicks, country, continent, pop_range, life_exp_range):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate
    
    # Filter the data based on user input
    filtered_data = data[(data['country'].isin(country) if country else True) &
                         (data['continent'].isin(continent) if continent else True) &
                         (data['pop'].between(pop_range[0], pop_range[1])) &
                         (data['lifeExp'].between(life_exp_range[0], life_exp_range[1]))]
    
    # Convert filtered data to CSV
    csv_string = filtered_data.to_csv(index=False, encoding='utf-8')
    
    # Create download link
    csv_string = "data:text/csv;charset=utf-8," + base64.b64encode(csv_string.encode()).decode()
    return dict(content=csv_string, filename="filtered_data.csv")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

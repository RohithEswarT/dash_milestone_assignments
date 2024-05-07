import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Import other pages
from input_test import app as input_field_page
from Dash_about_assignment import app as about_page
# from simulation_page import app as simulation_page

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout for the header
header = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
                    ],
                    align="center",
                ),
                href="/",
            ),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("About", href="/about")),
                    dbc.NavItem(dbc.NavLink("Input Field", href="/input-field")),
                    # dbc.NavItem(dbc.NavLink("Simulate", href="/simulation")),
                ],
                navbar=True,
                className="ml-auto",
            ),
        ]
    ),
    color="primary",
    dark=True,
)

# Define the layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    header,
    html.Div(id='page-content')
])

# Callback to render the correct page based on the URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/input-field':
        return input_field_page.layout
    elif pathname == '/about':
        return about_page.layout
    # elif pathname == '/simulation':
    #     return simulation_page.layout
    else:
        return about_page.layout  # Default to about page if invalid URL

if __name__ == '__main__':
    app.run_server(debug=True)

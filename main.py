import dcc as dcc
import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)
tab3_content = dbc.Card(
    dbc.CardBody(
        [
            "This is tab 1!"
        ]
    ),
    className="mt-3",
)
app.layout = dbc.Container([

    html.Div(id='container dev', children=[
        dcc.Loading([
            dcc.RadioItems(
                id='Selected Image',
                options=['TtW Total Emissions', 'TtW Emissions per Powertrain', 'TtW Consumption',
                         'WtW Total Emissions', 'WtW Sunburst 2021', 'WtW Sunburst 2035',
                         'LCA Total Emissions', 'LCA Waterfall', 'LCA Line Chart', 'LCA Scenario Chart'],
                value='TtW Total Emissions',
                inputStyle={"margin-left": "50px"},
                style={'color': '#00876C'}
            )
        ])
    ]),

    html.Div([
dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            tab3_content, label="Tab 3", disabled=False
        ),
    ]
),
        dbc.Row([  # Row 1
            dbc.Col(
                html.Div(html.Img(src='assets/kit_logo.png', width="50%")),
                width={"size": 3}
            ),
            dbc.Col(  # Column for headline
                html.H2(children=["CO", html.Sub(2), " Fleet Development Calculator"], className="header1",
                        style={'color': '#00876C', 'text-align': 'center'}),
                width={"size": 6}),
            dbc.Col(  # Column for picture
                html.Div(html.Img(src='assets/ifkm_logo.png', width="50%")),
                width={"size": 2, "offset": 1}
            ),
            dbc.Col(
                dbc.Switch("developer_options", label="Developer Options")
            )
        ])
    ]),
])






if __name__ == '__main__':
    app.run(debug=True)

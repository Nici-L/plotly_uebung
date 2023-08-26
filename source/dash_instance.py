import dash
import dash_bootstrap_components as dbc
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], assets_folder=os.getcwd() + "/assets")
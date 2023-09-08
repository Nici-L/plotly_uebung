from dash import html
import dash_bootstrap_components as dbc
import source.config as config

header_images = html.Div([
    dbc.Row([  # Row 1
        dbc.Col(
            html.Div(html.Img(src=f"kit_logo.png", width="25%")),
            width={"size": 2}
        ),
        dbc.Col(  # Column for headline
            html.H2(children=["CO", html.Sub(2), " Fleet Development Calculator"], className="header1",
                    style={'color': '#00876C', 'text-align': 'center'}),
            width={"size": 7}),
        dbc.Col(  # Column for picture
            html.Div(html.Img(src=f"{config.PICTURES_FOLDER_PATH}/ifkm_logo.png", width="25%")),
            width={"size": 2, "offset": 1}
        ),
    ])
])

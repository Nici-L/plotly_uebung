from dash import html
import dash_bootstrap_components as dbc
import source.config as config

header_images = html.Div([
    dbc.Row([  # Row 1
        dbc.Col(
            html.Div(
                html.Img(src=f"{config.PICTURES_FOLDER_PATH}/kit_logo.png", height="auto", width="100%")
            ),
            className="col-3",
            style={'height': '100%', 'text-align': 'center'}
        ),
        dbc.Col(  # Column for headline
            html.H2(children=["CO", html.Sub(2), " Fleet Development Calculator"],
                    className="header1 m-2 ms-5",
                    style={'color': '#00876c', 'text-align': 'center'}),
            className="col-6",
            style={'height': '100%', 'text-align': 'center', 'display': 'flex'}),
        dbc.Col(  # Column for picture
            html.Div(
                html.Img(src=f"{config.PICTURES_FOLDER_PATH}/ifkm_logo.png", height="100%", width="auto"),
                style={'height': '100%', 'width': '100%', 'text-align': 'end'},
            ),
            className="col-3",
            style={'height': '100%', 'text-align': 'center', 'display': 'flex'}
        ),
    ],
        style={'height': '100%', 'display': 'flex', 'text-align': 'center'},
    )
],
    style={'height': '130px', 'display': 'flex', 'text-align': 'center'},
    className="p-2 my-5"

)

import dash
import dash_bootstrap_components as dbc
import os
from matplotlib import pyplot as plt
import source.components.Tab_1.layout_header as header
from dash import html, dcc, Output, Input, State, no_update
import config as config
import utils.calculations as calc
import plotly.graph_objects as go
import plotly.express as px
import utils.colors_KIT_plotly as clr
from init_app import app
import source.components.Tab_1.figures as fig
from source.components.Tab_1 import callbacks as tab1_callbacks


# init app
# todo: Methoden Beschreibungen verbessern
# todo: ausgrauen bei dropdown wenn es option nicht gibt
# todo: genaue Zahlen an bars ergänzen
# todo: hover labels für Fahrzeugmodell

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], assets_url_path='/source/assets')

# get scenario options
# read all available csv files names
scenario_filenames = []
for file in os.listdir(config.SCENARIO_FOLDER_PATH):
    if file.endswith('.CSV') or file.endswith('.csv'):
        # scenario_filenames.append(file)
        scenario_filenames.append({
            'value': file,
            'label': file.replace('_', ' ').replace('.CSV', '').replace('.csv', '')
        })
print(f"scenario_filenames: {scenario_filenames}")

# use this in case the csv data has a lot of whitespaces
# initial_scenario_no_ws = initial_scenario.to_string().strip(' ')
# count_ws = pd.DataFrame(initial_scenario_no_ws, index=[0,1], columns=[1, 2])


# initial dashboard layout
app.layout = dbc.Container([
    dbc.Row([
        header.header_images,
    ]),
    dbc.Row([
        html.Div([
            dcc.Dropdown(options=scenario_filenames, id='scenario-dropdown', value=scenario_filenames[0].get('value'), className='Dropdown-2'),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(children="Select a scenario", id="output_input_div", className='m-2 callback-trigger-heading')
        ]),
    ]),
    dbc.Row([
        dbc.Col([html.Div([
            dbc.Accordion([
                dbc.AccordionItem([
                    dbc.Row([
                        html.Div("Share of fuel types", style={"font-weight": "bold", "font-size": "20px", "margin-top": "20px"}),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div('share of E5', id='share_E5_totalgasoline_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_E5", type="number", placeholder="share E5"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1"),
                        ]),
                        dbc.Col([
                            html.Div('share of E10', id='share_E10_totalgasoline_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_E10", type="number", placeholder="share E10"),  # style={'marginRight': '10px', "width":"16%"}
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share of diesel', id='share_diesel_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_diesel", type="number", placeholder="share diesel"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share of HVO', id='share_HVO_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_HVO", type="number", placeholder="share of HVO"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share of PtL', id='share_PtL_totaldiesel_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_PtL", type="number", placeholder="share PtL"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share of Bioliq', id='share_bioliq_totalgasoline_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_bioliq", type="number", placeholder="share Bioliq"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                    ]),
                    dbc.Row([
                        html.Div(['CO', html.Sub(2), 'e of the available fuel types'] , style={"font-weight": "bold", "font-size": "20px", "margin-top": "20px"}),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div(['CO', html.Sub(2), 'e E5'], id='co2e_E5_button', style={"font-weight": "bold"}),
                            dcc.Input(id="co2e_E5", type="number", placeholder=" E5", style={'marginRight': '10px', "width":"60%"}),
                            dbc.Badge("kg/l", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div(['CO', html.Sub(2), 'e E10'], id='co2e_E10_button', style={"font-weight": "bold"}),
                            dcc.Input(id="co2e_E10", type="number", placeholder="E10", style={'marginRight': '10px', "width":"60%"}),
                            dbc.Badge("kg/l", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div(['CO', html.Sub(2), 'e Diesel'], id='co2e_diesel_button', style={"font-weight": "bold"}),
                            dcc.Input(id="co2e_diesel", type="number", placeholder="B7", style={'marginRight': '10px', "width":"60%"}),
                            dbc.Badge("kg/l", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div(['CO', html.Sub(2), 'e HVO'], id='co2e_HVO_button', style={"font-weight": "bold"}),
                            dcc.Input(id="co2e_HVO", type="number", placeholder="HVO", style={'marginRight': '10px', "width":"60%"}),
                            dbc.Badge("kg/l", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div(['CO', html.Sub(2), 'e PtL'], id='co2e_PtL_button', style={"font-weight": "bold"}),
                            dcc.Input(id="co2e_PtL", type="number", placeholder="PtL", style={'marginRight': '10px', "width":"60%"}),
                            dbc.Badge("kg/l", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div(['CO', html.Sub(2), 'e bioliq'], id='co2e_bioliq_button', style={"font-weight": "bold"}),
                            dcc.Input(id="co2e_bioliq", type="number", placeholder="Bioliq", style={'marginRight': '10px', "width":"60%"}),
                            dbc.Badge("kg/l", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Div(['CO', html.Sub(2), 'e production of electricity'], id='co2e_electricity_button', style={"font-weight": "bold"}),
                                dcc.Input(id="co2e_electricity", type="number", placeholder="Emission electricity", style={'marginRight': '10px', "width":"20%"}),
                                dbc.Badge("g/kWh", color="dark", text_color="primary", className="ms-1")
                            ]),
                        ]),
                    ]),
                    dbc.Row([
                        html.Div("Share of vehicle type", style={"font-weight": "bold", "font-size": "20px", "margin-top": "20px"}),
                        ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div('vehicle stock', id='vehicle_stock_button', style={"font-weight": "bold"}),
                            dcc.Input(id="vehicle_stock", type="number", placeholder="vehicle stock"),
                            dbc.Badge("mio", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share icev_g', id='share_icev_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_icev_g", type="number", placeholder="share icev_g"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share icev_d', id='share_icev_d_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_icev_d", type="number", placeholder="share icev_d"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share hev', id='share_hev_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_hev", type="number", placeholder="share hev"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div('share phev',id='share_phev_button', style={"font-weight": "bold"}),
                            dcc.Input(id="share_phev", type="number", placeholder="share phev"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                        dbc.Col([
                            html.Div('share bev',id='share_bev_button', style={"font-weight": "bold"} ),
                            dcc.Input(id="share_bev", type="number", placeholder="share_bev"),
                            dbc.Badge("%", color="dark", text_color="primary", className="ms-1")
                        ]),
                    ]),
                    html.Div([
                               dbc.Button(id='calculate-button', n_clicks=0, children='calculate', color='success', size='lg', class_name='m-3 calculate-button'),
                               dbc.Button(id='reset-button', n_clicks=0, children='reset', color='success', size='lg', class_name='m-3 calculate-button')
                           ]),
                    ], title='parameter menu', class_name='m-3'),
                ], start_collapsed=True, className='parameter-Accordion')
            ]),
        ]),
    ]),
    dbc.Col([
        dbc.Accordion([
            dbc.AccordionItem([dbc.Button("What is TtW?", id="open-xl", n_clicks=0, className='button'),
                               dbc.Modal([
                                   dbc.ModalHeader(dbc.ModalTitle("TtW")),
                                   dbc.ModalBody("TtW is an abreviation for Tank to Wheel and describes the boundaries of the Calculation. Tank to Wheel means, only the emissions the car is emitting between the tank and the wheel is being taken into account"),
                               ], id="modal-xl", size="xl", is_open=False),
                               ], title='Information about the dashboard', class_name='m-3')
        ], start_collapsed=True)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                children=[
                    dbc.Label("Select a LCA calculation"),
                    dcc.Dropdown(options=['TtW', 'WtW'], id='display_figure', value='TtW', className='Dropdown-2'),
                    dcc.Graph(id='co2e_ttw_barchart', figure=fig.get_fig_sum_total_co2e(fig.co2e_ttw_per_segment, fig.selected_scenario), className='mt-5'),
                ]
            ),
            html.Div(
                [
                    dbc.Button(
                        "More Information about the graph",
                        id="collapse-button-1",
                        className="m-5 collapse-button",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dbc.Card(dbc.CardBody("The Co<sub>2e</sub> emissions of Germany are defined by the government. This official number was taken and multiplied with 68% which is the share passenger cars hold on total Co2e emissions caused by traffic.")),
                        id="collapse",
                        is_open=False,
                    ),
                ], className='collapse-div1 mr-3'
            )
        ]
        ),
        dbc.Col([
            html.Div(
                children=[
                    dbc.Label("Select a segment and calculation"),
                    dbc.Alert("In case of small numbers hover over the graph!", color="danger", dismissable=True, className='small-number-warning'),
                    dcc.Dropdown(options=fig.selected_scenario.index.get_level_values(1).unique(), id='choose-segments', value='Mini', searchable=False, className='Dropdown-2'),
                    dcc.Dropdown(options=['one car', 'all vehicles'], id='one_car_dropdown', value='all vehicles', className='Dropdown-2'),
                    dcc.Dropdown(options=['TtW', 'WtW'], id='TtW_vehicle_class_fig', value='TtW', className='Dropdown-2'),
                    dcc.Graph(id='co2e_ttw_barchart_car', figure=fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_ttw_per_segment_df, 'Kleinwagen'), className='mt-4')
                ]
            ),
            html.Div(
                [
                    dbc.Button(
                        "More Information about the graph",
                        id="collapse-button-2",
                        className="collapse-button",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dbc.Card(dbc.CardBody([
                            html.H5('Data for vehicle stock:', className="fw-bold"),
                            html.P("Kraftfahrbundesamt"),
                            html.H5("Calculation:"),
                            html.P("co2e emitted during usage multiplied with average consumption per segment")
                        ])
            ),
                        id="collapse 2",
                        is_open=False,
                    ),
                ], className='collapse-div1 mr-3'
            )
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Accordion([
                dbc.AccordionItem([html.Div(
                    children=[
                        dbc.Label("Select a vehicle class and segment"),
                        dcc.Dropdown(options=['kWh', 'liter'], id='kWh-or-liter', value='liter', className='Dropdown-2'),
                        dcc.Dropdown(options=fig.selected_scenario.index.get_level_values(0).unique(), id='consumption-vehicle-class', multi=True, value=['icev'], className='Dropdown-2'),
                        dcc.Dropdown(options=fig.selected_scenario.index.get_level_values(1).unique(), id='consumption-segment', multi=True, value=['Mini', 'Kleinwagen'], className='Dropdown-2'),
                        dcc.Graph(id='fig-consumption', figure=fig.get_fig_consumption(fig.selected_scenario, ['Mini', 'Kleinwagen'], 'icev')),
                        html.Div(
                            [
                                dbc.Button(
                                    "More Information about the graph",
                                    id="collapse-button-3",
                                    className="mb-3 collapse-button",
                                    color="primary",
                                    n_clicks=0,
                                ),
                                dbc.Collapse(
                                    dbc.Card(dbc.CardBody(
                                        "Data: ADAC")),
                                    id="collapse 3",
                                    is_open=False,
                                ),
                            ], className='collapse-div1 mr-3'
                        )
                    ]
                )
                ], title='Graph showing the consumption of different vehicles')
                ], start_collapsed=True, className='m-5'
            ),

        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                children=[
                    dbc.Label('Choose the scenarios'),
                    dcc.Dropdown(options=scenario_filenames, id='scenario-dropdown-comparison', multi=True, value=scenario_filenames[0].get('value'), className='Dropdown-2'),
                    dcc.Dropdown(options=['TtW', 'WtW'], id='chose_lca_comparison_fig', value='TtW', className='Dropdown-2'),
                    dbc.Switch(label='Show production and recycling per car', value=True, id='details-toggle-option', className='recycling_toggle_switch'),
                    dcc.Graph(id='scenario-comparison', figure={}, className='mt-5 scenario_comparison_fig')
                ]
            ),
            html.Div(
                [
                    dbc.Button(
                        "More Information about the graph",
                        id="collapse-button-4",
                        className="mb-3 collapse-button",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dbc.Card(dbc.CardBody(
                            "noch Leer")),
                        id="collapse 4",
                        is_open=False,
                    ),
                ], className='collapse-div1 mr-3'
            )
        ]),
        dbc.Col([
            html.Div(
              children=[
                  dbc.Label('Select the car you want to see a detailed LCA of'),
                  dcc.Dropdown(options=scenario_filenames, id='scenario-dropdown-lca', value=scenario_filenames[0].get('value'), className='Dropdown-2'),
                  dcc.Dropdown(options=['TtW', 'WtW'], id='chose_lca', value='TtW', className='Dropdown-2'),
                  dcc.Dropdown(options=fig.selected_scenario.index.get_level_values(0).unique(), id='lca-vehicle-class', value='icev', className='Dropdown-2'),
                  dcc.Dropdown(options=fig.selected_scenario.index.get_level_values(1).unique(), id='lca-segment', value='Mini', className='Dropdown-2'),
                  dbc.Switch(label='Include recycling', value=True, id='recycling-option', className='recycling_toggle_switch'),
                  dbc.Button(id='selection-button', n_clicks=0, children='apply selection', color='success', size='m', class_name='m-3 selection-button'),
                  dcc.Graph(id='lca-waterfall-fig', figure=fig.get_fig_lca_waterfall(scenario_filenames[0].get('value'), chosen_lca='ttw', chosen_vehicle_class='icev', chosen_segment='Mini', is_recycling_displayed=True))
              ]
            ),
            html.Div(
                [
                    dbc.Button(
                        "More Information about the graph",
                        id="collapse-button-5",
                        className="mb-3 collapse-button",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dbc.Card(dbc.CardBody(
                            "Data: Umweltbundesamt Aut")),
                        id="collapse 5",
                        is_open=False,
                    ),
                ], className='collapse-div1 mr-3'
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(options=['TtW', 'WtW'], id='chose_lca_scatter_plot', value='TtW', className='Dropdown-2'),
                dcc.Dropdown(options=fig.selected_scenario.index.get_level_values(1).unique(), id='lca-segment-production-comparison', value='Mittelklasse', className='Dropdown-2'),
                dcc.Dropdown(options=['per year', 'per km'], id='chose_km_or_year', value='per year', className='Dropdown-2'),
                dcc.Graph(id='fig_production_comparison', figure=fig.get_fig_production_comparison_per_year(co2_per_car=fig.co2e_ttw_per_car, segment='Mittelklasse'))
            ], className='mr-3')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='co2e_over_the_years_fig', figure=fig.get_yearly_co2_fig())
        ])
    ])
])



if __name__ == '__main__':
    tab1_callbacks.register_callbacks(app)
    app.run(debug=True)

# todo:  https://dash.plotly.com/background-callbacks#:~:text=debug%3DTrue)-,Example%202%3A%20Disable%20Button%20While%20Callback%20Is%20Running,-Notice%20how%20in
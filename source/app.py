import dash
import dash_bootstrap_components as dbc
import os
import pandas as pd
import source.components.Tab_1.layout_header as header
from dash import html, dcc, Output, Input, State, no_update
import config as config
import utils.calculations as calc
import plotly.graph_objects as go
import plotly.express as px


# init app
# todo: grafik aufhübschen, Meldung wenn Werte arg klein sind (Modal Button?) (x-mal kleiner als größter Wert) und man sie deshalb nicht sieht, emission targets ergänzen
# todo: Methoden Beschreibungen verbessern
# todo: autosize in consumption diagram?
# todo: calculate button farbe ändern und zentrieren, margin um calculator button, margin um parameter menu, farben der diagramme,
# todo: Methode schreiben die schon summiert und mit emission targets eine eigene kleine series bildet

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], assets_folder=os.getcwd() + 'source/assets')

# get scenario options
# read all available csv files names
scenario_filenames = []
for file in os.listdir(config.SCENARIO_FOLDER_PATH):
    if file.endswith('.CSV') or file.endswith('.csv'):
        scenario_filenames.append(file)
print(f"scenario_filenames: {scenario_filenames}")
# beautify names

# get all necessary data to display initial scenario
# read in initial scenario data
# initial_scenario = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{scenario_filenames[0]}', sep=';', decimal=",", thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])

# initial_scenario_no_ws = initial_scenario.to_string().strip(' ')
# count_ws = pd.DataFrame(initial_scenario_no_ws, index=[0,1], columns=[1, 2])


# initialize global variables
selected_scenario: pd.DataFrame
consumption_per_year_liter: pd.Series
consumption_per_year_kwh: pd.Series
consumption_per_year_liter_with_energy_supply: pd.Series
consumption_per_year_kWh_with_energy_supply: pd.Series
co2e_ttw_per_car: pd.Series
co2e_ttw_per_segment: pd.Series
co2e_ttw_per_segment_df: pd.DataFrame
co2e_wtw_per_car: pd.Series
co2e_wtw_per_segment: pd.Series
co2e_wtw_per_segment_df: pd.DataFrame
co2e_production_one_car: pd.Series
co2e_savings_one_car: pd.Series


def init_global_variables(selected_scenario_name: str):
    # read in initial scenario data
    global selected_scenario
    selected_scenario = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{selected_scenario_name}', sep=';', decimal=",",
                                   thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
    # calculating consumption per year
    global consumption_per_year_liter
    consumption_per_year_liter = calc.calculate_yearly_consumption_liter(selected_scenario)
    global consumption_per_year_kwh
    consumption_per_year_kwh = calc.calculate_yearly_consumption_kwh(selected_scenario)
    # add energy supply column
    global consumption_per_year_liter_with_energy_supply
    consumption_per_year_liter_with_energy_supply = consumption_per_year_liter.to_frame('consumption_manufacturer_l').join(selected_scenario['energysupply'])
    global consumption_per_year_kWh_with_energy_supply
    consumption_per_year_kWh_with_energy_supply = consumption_per_year_kwh.to_frame('consumption_manufacturer_kWh').join(selected_scenario['energysupply'])
    # calculating co2e ttw per year per car
    global co2e_ttw_per_car
    co2e_ttw_per_car = calc.get_co2e_usage_ttw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, selected_scenario)
    # calculating co2e ttw per year per segment
    global co2e_ttw_per_segment
    co2e_ttw_per_segment = calc.get_co2e_usage_ttw_per_segment(co2e_ttw_per_car, selected_scenario)
    global co2e_ttw_per_segment_df
    co2e_ttw_per_segment_df = co2e_ttw_per_segment.to_frame('co2e')
    # calculating co2e wtw per year per car
    global co2e_wtw_per_car
    co2e_wtw_per_car = calc.get_co2e_usage_wtw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, selected_scenario)
    # calculating co2e wtw per year per segment
    global co2e_wtw_per_segment
    co2e_wtw_per_segment = calc.get_co2e_usage_wtw_per_segment(co2e_wtw_per_car, selected_scenario)
    global co2e_wtw_per_segment_df
    co2e_wtw_per_segment_df = co2e_wtw_per_segment.to_frame('co2e')
    # calculating co2e of production for one car
    global co2e_production_one_car
    co2e_production_one_car = calc.calculate_production_co2e_per_car(selected_scenario)
    # calculate co2e savings (recycling)
    global co2e_savings_one_car
    co2e_savings_one_car = calc.calculate_co2e_savings(selected_scenario)


init_global_variables(scenario_filenames[3])


def get_fig_sum_total_co2e(co2e_series, dataframe):
    print(dataframe.columns)
    fig_sum_total_co2e = go.Figure(data=[
        go.Bar(
                x=['co2e'],
                y=[co2e_series.sum()],
            ),
    ],
            layout={  # dictionary 'key':'value'
                'barmode': 'relative',
                'title': 'CO2e of different vehicle segments in kg',
                'template': 'ggplot2',
                'plot_bgcolor': '#002b36',  # color Solar stylesheet
                'paper_bgcolor': '#002b36',
                'font_color': 'white',
                'width': 500,
                'height': 450,
                }
            )
    fig_sum_total_co2e.update_yaxes(range=[0, 100000000000], autorange=False)
    emission_target_2030 = dataframe['new_emission_targets_germany_2030_fleet'].iloc[0]
    emission_target_2030_only_pkw = emission_target_2030 * 0.68
    fig_sum_total_co2e.add_trace(
        go.Bar(
            x=['co2e_2030'],
            y=[emission_target_2030_only_pkw],
        )
    )
    return fig_sum_total_co2e


def get_fig_co2e_segment_all_vehicle_classes(co2e_dataframe, chosen_segment):
    x_val = co2e_dataframe.loc[(slice(None), f"{chosen_segment}"), "co2e"]
    fig_co2e_segment_all_vehicle_classes = px.bar(x_val.to_frame('co2e'), x=x_val.to_frame('co2e').index.get_level_values(0), y='co2e')
    fig_co2e_segment_all_vehicle_classes .update_layout(
            plot_bgcolor='#002b36',  # color Solar stylesheet
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='relative',
            hovermode="x unified")
    fig_co2e_segment_all_vehicle_classes.update_yaxes(range=[0, 8000000000], autorange=False)
    return fig_co2e_segment_all_vehicle_classes


def get_fig_consumption(co2e_dataframe, chosen_segments, chosen_vehicle_class):
    consumption_segments = co2e_dataframe.loc[(chosen_vehicle_class, chosen_segments), "consumption_manufacturer_l"].to_frame('consumption')
    fig_consumption = px.bar(data_frame=consumption_segments, y=consumption_segments.index.get_level_values(0), x='consumption', orientation='h', barmode='group', color=consumption_segments.index.get_level_values(1))
    fig_consumption.update_layout(
            plot_bgcolor='#002b36',  # color Solar stylesheet
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='group',
            autosize=True,
    )
    return fig_consumption

# y_val = initial_scenario.loc[(slice(None), "Mini"), "consumption_manufacturer_l"]
# y_val_2 = initial_scenario.loc[(slice(None), "Kleinwagen"), "consumption_manufacturer_l"]
# y_val_together = pd.concat([y_val_2, y_val], axis=1)


# initial dashboard layout
app.layout = dbc.Container([
    dbc.Row([
        header.header_images,
    ]),
    dbc.Row([
        html.Div([
            dcc.Dropdown(options=scenario_filenames, id='scenario-dropdown', value=scenario_filenames[3]),
        ]),
    ]),
    dbc.Row([
        dbc.Col([html.Div([
            dbc.Accordion([
                dbc.AccordionItem([
                           dbc.Button(id='consumption_manufacturer_l-button', n_clicks=0, children='consumption_manufacturer_l', color='primary', class_name='m-2'),
                           dbc.Button(id='share_E5_totalgasoline-button', n_clicks=0, children='share_E5_totalgasoline', color='primary', class_name='m-2'),
                           dbc.Button(id='co2e_E5_TtW-button', n_clicks=0, children='co2e_E5_TtW', color='primary', class_name='m-2'),
                           dbc.Button(id='vehicle_stock-button', n_clicks=0, children='vehicle_stock', color='primary', class_name='m-2'),
                           dbc.Button(id='glider_weight-button', n_clicks=0, children='glider_weight', color='primary', class_name='m-2'),
                           dbc.Button(id='co2e_production-button', n_clicks=0, children='co2e_production', color='primary', class_name='m-2'),
                           dbc.Button(id='power_electric_engine-button', n_clicks=0, children='power_electric_engine', color='primary', class_name='m-2'),
                           dbc.Button(id='battery_capacity_brutto-button', n_clicks=0, children='battery_capacity_brutto', color='primary', class_name='m-2'),
                           dbc.Button(id='co2e_battery_production-button', n_clicks=0, children='co2e_battery_production', color='primary', class_name='m-2'),
                           dbc.Button(id='co2e_savings_glider-button', n_clicks=0, children='co2e_savings_glider', color='primary', class_name='m-2'),
                           dbc.Button(id='co2e_savings_battery-button', n_clicks=0, children='co2e_savings_battery', color='primary', class_name='m-2'),
                    ], title='parameter menu accordion'),
                ], start_collapsed=True,)
            ]),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(id='calculate-button', n_clicks=0, children='calculate', color='secondary', size='lg', class_name='m-3')
            ])], class_name='align-middle'),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                children=[
                    dbc.Label("Options"),
                    dcc.Dropdown(options=['TtW', 'WtW'], id='display_figure', value='TtW'),
                    dcc.Graph(id='co2e_ttw_barchart', figure=get_fig_sum_total_co2e(co2e_ttw_per_segment, selected_scenario)),
                    # todo: add germany target
                ]
            )
        ], width=4
        ),
        dbc.Col([
            html.Div(
                children=[
                    dbc.Label("Please select a segment"),
                    dcc.Dropdown(selected_scenario.index.get_level_values(1).unique(), id='choose-segments', value='Mini', searchable=False),
                    dcc.Dropdown(options=['TtW', 'WtW'], id='TtW_vehicle_class_fig', value='TtW'),
                    dcc.Graph(id='co2e_ttw_barchart_car', figure=get_fig_co2e_segment_all_vehicle_classes(co2e_ttw_per_segment_df, 'Kleinwagen'))
                ]
            )
        ]),
        dbc.Col([
            html.Div(
                children=[
                    dbc.Label("Please select a vehicle class and segment"),
                    dcc.Dropdown(selected_scenario.index.get_level_values(0).unique(), id='consumption-vehicle-class', multi=True, value=['icev']),
                    dcc.Dropdown(selected_scenario.index.get_level_values(1).unique(), id='consumption-segment', multi=True, value=['Mini', 'Kleinwagen']),
                    dcc.Graph(id='fig-consumption', figure=get_fig_consumption(selected_scenario, ['Mini', 'Kleinwagen'], 'icev'))
                ] #todo: Dropdown for electricity consumption
            )
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(
                children=[
                    dbc.Label('Choose the scenarios'),
                    dcc.Dropdown(options=scenario_filenames, id='scenario-dropdown-comparison', multi=True, value=scenario_filenames[0]),
                    dcc.Graph(id='scenario-comparison')
                ]
            )
        ])
    ])
])


# callback for scenario dropdown
@app.callback([
    Output(component_id='co2e_ttw_barchart', component_property='figure', allow_duplicate=True),
    Output(component_id='co2e_ttw_barchart_car', component_property='figure', allow_duplicate=True)],
    Input(component_id='calculate-button', component_property='n_clicks'),
    [State(component_id='scenario-dropdown', component_property='value')],
    prevent_initial_call=True
)
def update_graph(n, scenario_chosen):
    init_global_variables(scenario_chosen)

    fig_sum_total_co2e = get_fig_sum_total_co2e(co2e_ttw_per_segment, selected_scenario)

    fig_co2e_segment_all_vehicle_classes = get_fig_co2e_segment_all_vehicle_classes(co2e_ttw_per_segment_df, 'Kleinwagen')

    fig_consumption = get_fig_consumption(selected_scenario, ['Mini', 'Kleinwagen'], 'icev')

    return fig_sum_total_co2e, fig_co2e_segment_all_vehicle_classes, fig_consumption


# callback for TtW or WtW button
@app.callback(
    Output("co2e_ttw_barchart", "figure"),
    [Input("display_figure", "value")],
    prevent_initital_call=True
)
def make_graph(display_figure):
    if display_figure == 'TtW':
        fig_sum_total_co2e = get_fig_sum_total_co2e(co2e_ttw_per_segment, selected_scenario)
        return fig_sum_total_co2e
    elif display_figure == 'WtW':
        fig_sum_total_co2e = get_fig_sum_total_co2e(co2e_wtw_per_segment, selected_scenario)
    else:
        fig_sum_total_co2e = {}
    return fig_sum_total_co2e


# callback for segment and TtW dropdown
@app.callback(
    Output('co2e_ttw_barchart_car', 'figure'),
    [Input('TtW_vehicle_class_fig', 'value'),
     Input('choose-segments', 'value')],
)
def update_car_graph(chosen_lc_step, chosen_segment):
    if chosen_lc_step == 'TtW':
        fig_co2e_segment_all_vehicle_classes = get_fig_co2e_segment_all_vehicle_classes(co2e_ttw_per_segment_df, chosen_segment)
        return fig_co2e_segment_all_vehicle_classes
    elif chosen_lc_step == 'WtW':
        fig_co2e_segment_all_vehicle_classes = get_fig_co2e_segment_all_vehicle_classes(co2e_wtw_per_segment_df, chosen_segment)
        return fig_co2e_segment_all_vehicle_classes
    else:
        fig_co2e_segment_all_vehicle_classes = {}
    return fig_co2e_segment_all_vehicle_classes


# callback for segment and vehicle class dropdown
@app.callback(
    Output('fig-consumption', 'figure'),
    [Input('consumption-segment', 'value'),
     Input('consumption-vehicle-class', 'value')],
    prevent_initial_call=True
)
def update_consumption_graph(chosen_segments, chosen_vehicle_class):
    if chosen_vehicle_class is None or len(chosen_vehicle_class) == 0 and chosen_segments is None or len(chosen_segments) == 0 or None:
        return no_update
    elif len(chosen_vehicle_class) == 0 and len(chosen_segments) == 1:
        fig_consumption = get_fig_consumption(selected_scenario, chosen_segments, slice(None))
        return fig_consumption
    elif len(chosen_vehicle_class) >= 1 and len(chosen_segments) == 1:
        fig_consumption = get_fig_consumption(selected_scenario, chosen_segments, chosen_vehicle_class)
        return fig_consumption
    elif len(chosen_vehicle_class) >= 1 and len(chosen_segments) >= 1:
        fig_consumption = get_fig_consumption(selected_scenario, chosen_segments, chosen_vehicle_class)
        return fig_consumption
    else:
        return no_update    # chosen_vehicle_class, chosen_segments

'''
# callback for scenario comparison
@app.callback(
    Output('scenario-comparison', 'figure'),
    Input('scenario-dropdown-comparison', 'value'),
    prevent_initital_call=True
)
def update_comparison_graph(chosen_scenario_list):
    if not type(chosen_scenario_list) == list:
        chosen_scenario_list = [chosen_scenario_list]
    fig_comparison = go.Figure()
    for scenario in chosen_scenario_list:
        init_global_variables(scenario)
        fig_comparison.add_trace(go.Bar(
            y=[scenario],
            x=[co2e_ttw_per_segment.sum()],
            orientation='h'
        ))
        fig_comparison.update_layout(
            legend_title_text="LCA",
            plot_bgcolor='#002b36',  # color Solar stylesheet
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='group',
            autosize=True,
            # width=500,
            # height=450,
        )
        fig_comparison.update_xaxes(title_text="Comparison between different scenarios")
        fig_comparison.update_yaxes(title_text="Scenarios")
    return fig_comparison
'''

if __name__ == '__main__':
    app.run(debug=True)

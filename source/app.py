import dash
import dash_bootstrap_components as dbc
import os
import pandas as pd
import source.components.Tab_1.layout_header as header
from dash import html, dcc, Output, Input, State
import config as config
import utils.calculations as calc
import plotly.graph_objects as go
import plotly.express as px
# init app
# todo: grafik aufhübschen, Meldung wenn Werte arg klein sind (x-mal kleiner als größter Wert) und man sie deshalb nicht sieht

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
initial_scenario: pd.DataFrame
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
    global initial_scenario
    initial_scenario = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{selected_scenario_name}', sep=';', decimal=",",
                                   thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
    # calculating consumption per year
    global consumption_per_year_liter
    consumption_per_year_liter = calc.calculate_yearly_consumption_liter(initial_scenario)
    global consumption_per_year_kwh
    consumption_per_year_kwh = calc.calculate_yearly_consumption_kwh(initial_scenario)
    # add energy supply column
    global consumption_per_year_liter_with_energy_supply
    consumption_per_year_liter_with_energy_supply = consumption_per_year_liter.to_frame('consumption_manufacturer_l').join(initial_scenario['energysupply'])
    global consumption_per_year_kWh_with_energy_supply
    consumption_per_year_kWh_with_energy_supply = consumption_per_year_kwh.to_frame('consumption_manufacturer_kWh').join(initial_scenario['energysupply'])
    # calculating co2e ttw per year per car
    global co2e_ttw_per_car
    co2e_ttw_per_car = calc.get_co2e_usage_ttw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, initial_scenario)
    # calculating co2e ttw per year per segment
    global co2e_ttw_per_segment
    co2e_ttw_per_segment = calc.get_co2e_usage_ttw_per_segment(co2e_ttw_per_car, initial_scenario)
    global co2e_ttw_per_segment_df
    co2e_ttw_per_segment_df = co2e_ttw_per_segment.to_frame('co2e')
    # calculating co2e wtw per year per car
    global co2e_wtw_per_car
    co2e_wtw_per_car = calc.get_co2e_usage_wtw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, initial_scenario)
    # calculating co2e wtw per year per segment
    global co2e_wtw_per_segment
    co2e_wtw_per_segment = calc.get_co2e_usage_wtw_per_segment(co2e_wtw_per_car, initial_scenario)
    global co2e_wtw_per_segment_df
    co2e_wtw_per_segment_df = co2e_wtw_per_segment.to_frame('co2e')
    # calculating co2e of production for one car
    global co2e_production_one_car
    co2e_production_one_car = calc.calculate_production_co2e_per_car(initial_scenario)
    # calculate co2e savings (recycling)
    global co2e_savings_one_car
    co2e_savings_one_car = calc.calculate_co2e_savings(initial_scenario)


init_global_variables(scenario_filenames[0])


fig = px.bar(co2e_ttw_per_segment_df, x=co2e_ttw_per_segment_df.index.get_level_values(0), y='co2e',
             color=co2e_ttw_per_segment_df.index.get_level_values(1))
x_val = co2e_ttw_per_segment_df.loc[(slice(None), 'Kleinwagen'), "co2e"]
fig2 = px.bar(x_val.to_frame('co2e'), x=x_val.to_frame('co2e').index.get_level_values(0), y='co2e')

print(co2e_ttw_per_segment_df.loc[(slice(None), 'Kleinwagen'), "co2e"])
print(co2e_ttw_per_segment_df.query("segments == 'Kleinwagen'"))


# initial dashboard layout
app.layout = dbc.Container([
    dbc.Row([
        header.header_images,
    ]),
    dbc.Row([
        html.Div([
            dcc.Dropdown(options=scenario_filenames, id='scenario-dropdown', value=scenario_filenames[0]),
        ]),
    ]),
    dbc.Row([
        dbc.Col([html.Div([
            dbc.Accordion([
                dbc.AccordionItem([
                    html.P('This is going to be the parameter menu')
                ], title='parameter menu accordion'),
            ])
        ]), ]),
    ]),
    dbc.Row([
        dbc.Col([html.Div([
            dbc.Button(id='calculate-button', n_clicks=0, children='calculate', color='secondary', size='lg',
                       className='me-3')
        ]), ]),
    ]),
    dbc.Row([
        html.Div(
            children=[
                dbc.Label("Options"),
                dcc.RadioItems(id="display_figure", options=[{'label': 'TtW', 'value': 'Figure1'}, {'label': 'WtW', 'value': 'Figure2'}], value='Figure1')
            ]
        ),
    ]),
    dbc.Row([
        html.Div(
            children=[
                dcc.Graph(id='co2e_ttw_barchart', figure={}),
            ]
        )
    ]),
    dbc.Row([
        html.Div(
            children=[
                dbc.Label("Options"),
                dcc.Dropdown(initial_scenario.index.get_level_values(1).unique(), id='choose-segments', value='Mini'),
                dcc.Graph(id='co2e_ttw_barchart_car', figure={})
            ]
        ),
    ]),
])

'''
@app.callback(
    Output('raw_data_table_container', 'children'),
    Input(component_id='calculate-button', component_property='n_clicks'),
    [State(component_id='scenario-dropdown', component_property='value')],
)
def update_table(n, file_name):
    print(n)
    selected_scenario_raw_data = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{file_name}', sep=';', decimal=",", thousands='.',
                                             encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
    updated_table = dbc.Table.from_dataframe(id='raw_data_table', df=selected_scenario_raw_data, striped=True,
                                             bordered=True, hover=True, index=True)
    return updated_table

'''


@app.callback([
    Output(component_id='co2e_ttw_barchart', component_property='figure', allow_duplicate=True),
    Output(component_id='co2e_ttw_barchart_car', component_property='figure', allow_duplicate=True)],
    Input(component_id='calculate-button', component_property='n_clicks'),
    [State(component_id='scenario-dropdown', component_property='value')],
    prevent_initial_call=True
)
def update_graph(n, scenario_chosen):
    init_global_variables(scenario_chosen)
    fig3 = px.bar(co2e_ttw_per_segment_df, x=co2e_ttw_per_segment_df.index.get_level_values(0), y='co2e', color=co2e_ttw_per_segment_df.index.get_level_values(1))
    fig4 = px.bar(x_val.to_frame('co2e'), x=x_val.to_frame('co2e').index.get_level_values(0), y='co2e')
    print(n)
    return fig3, fig4


@app.callback(
    Output("co2e_ttw_barchart", "figure"),
    [Input("display_figure", "value")],
    prevent_initital_call=True
)
def make_graph(display_figure):
    # print(display_figure)
    if 'Figure1' in display_figure:
        fig6 = px.bar(co2e_ttw_per_segment_df, x=co2e_ttw_per_segment_df.index.get_level_values(0), y='co2e', color=co2e_ttw_per_segment_df.index.get_level_values(1))
        return fig6
    elif 'Figure2' in display_figure:
        fig6 = px.bar(co2e_wtw_per_segment_df, x=co2e_wtw_per_segment_df.index.get_level_values(0), y='co2e', color=co2e_wtw_per_segment_df.index.get_level_values(1))
        # return fig
    else:
        fig6 = {}
    return fig6


@app.callback(
    Output('co2e_ttw_barchart_car', 'figure'),
    Input('choose-segments', 'value'),
)
def update_car_graph(chosen_segment):
    fig7 = {}
    x_value = co2e_ttw_per_segment_df.loc[(slice(None), f"{chosen_segment}"), "co2e"]
    fig7 = px.bar(x_value.to_frame('co2e'), x=x_value.to_frame('co2e').index.get_level_values(0), y='co2e')
    # fig7 = px.bar(co2e_ttw_per_segment_df, x=co2e_ttw_per_segment_df.loc[(slice(None), f"{chosen_segment}"), "co2e"], y='co2e',
                      # color=co2e_ttw_per_segment_df.index.get_level_values(0))
    return fig7


if __name__ == '__main__':
    app.run(debug=True)

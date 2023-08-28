import dash
import dash_bootstrap_components as dbc
import os
import pandas as pd
import source.components.Tab_1.layout_header as header
from dash import html, dcc, Output, Input
import config as config
import utils.calculations as calc
# init app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], assets_folder=os.getcwd() + "/assets")

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
initial_scenario = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{scenario_filenames[2]}', sep=';', decimal=",", thousands='.',
                                         encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])

# initial_scenario_no_ws = initial_scenario.to_string().strip(' ')
# count_ws = pd.DataFrame(initial_scenario_no_ws, index=[0,1], columns=[1, 2])

# function only displaying consumption


# calculating consumption per year
consumption_per_year_liter = calc.calculate_yearly_consumption_liter(initial_scenario)
print(f"consumption_liter_per_year  {consumption_per_year_liter}")
consumption_per_year_kwh = calc.calculate_yearly_consumption_kwh(initial_scenario)
print(f"consumption_kwh_per_year  {consumption_per_year_kwh}")


# add energy supply column
consumption_per_year_liter_with_energy_supply = consumption_per_year_liter.to_frame('consumption_manufacturer_l').join(initial_scenario['energysupply'])
print(f"energy supply spalte zu liter series: {consumption_per_year_liter_with_energy_supply}")
consumption_per_year_kWh_with_energy_supply = consumption_per_year_kwh.to_frame('consumption_manufacturer_kWh').join(initial_scenario['energysupply'])
print(f"energy supply spalte zu kwh series: {consumption_per_year_kWh_with_energy_supply}")

# calculating co2e per year
# if Abfrage
calc.get_co2e_usage_ttw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, initial_scenario)


# initial dashboard layout
app.layout = dbc.Container([
    header.header_images,
    html.Div([
        dcc.Dropdown(options=scenario_filenames, id='scenario-dropdown'),
    ]),
    html.Div([
        dbc.Accordion([
            dbc.AccordionItem([
                html.P('This is going to be the parameter menu')
            ], title='parameter menu accordion'),
        ])
    ]),
    html.Div(
        id='raw_data_table_container',
        children=[
            dbc.Table.from_dataframe(id='raw_data_table', df=initial_scenario, striped=True, bordered=True,
                                     hover=True, index=True),
        ]
    )
])


@app.callback(
    Output('raw_data_table_container', 'children'),
    Input('scenario-dropdown', 'value')
)
def update_table(file_name):
    # Replace this with your actual data retrieval logic
    selected_scenario_raw_data = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{file_name}', sep=';', decimal=",", thousands='.',
                                             encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
    updated_table = dbc.Table.from_dataframe(id='raw_data_table', df=selected_scenario_raw_data, striped=True,
                                             bordered=True, hover=True, index=True)
    return updated_table


if __name__ == '__main__':
    app.run(debug=True)
from dash import html, dcc, Input, Output, callback, Dash, dash_table
from dash.dependencies import Input, Output
import os
import dash_bootstrap_components as dbc
from source.dash_instance import app
import pandas as pd
import source.components.Tab_1.layout_header as header
# import source.components.Tab_1.icev_figures.figure_component_icev as bar_charts
# import source.components.Tab_1.total_co2e_passenger_cars.figure_components_total_passenger_cars as total_passenger_cars
# import source.components.Tab_1.lkw_figures.figure_component_heavy_duty as heavy_duty
from source.utils import calculations as calc_util

folder_path = 'assets/data'
output_file = 'output.csv'

# list of all the csv files in data folder
csv_files = []
for file in os.listdir(folder_path):
    if file.endswith('.CSV') or file.endswith('.csv'):
        csv_files.append(file)
print(f"csv files: {csv_files}")

# read csv file in by using the csv file list and the folder path
selected_scenario_raw_data = pd.read_csv(f'{folder_path}/{csv_files[0]}', sep=';', decimal=",", thousands='.',
                                         encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
selected_scenario_raw_data: pd.DataFrame  # helpful for pycharm

#print(selected_scenario_raw_data['vehicle class'])

# pass dataframe as a parameter here
'''def whitespace_remover(dataframe):
    # iterating over the columns
    for i in dataframe.columns:
        # checking datatype of each column
        if dataframe[i].dtype == 'object':
            # applying strip function on column
            try:
                dataframe[i] = dataframe[i].map(str.strip)
            except Exception as e:
                print(f"Found float or int: {dataframe[i]}")
        else:
            # if condn. is False then it will do nothing.
            pass

# applying whitespace_remover function on dataframe
whitespace_remover(selected_scenario_raw_data)'''

selected_scenario_raw_data_no_ws = selected_scenario_raw_data.replace(' ', '')


# Define function to remove extra whitespace
def remove_whitespace(s):
    return ' '.join(s.split())


# Apply function to desired column
#selected_scenario_raw_data[1] = selected_scenario_raw_data[1].apply(remove_whitespace)

# Save cleaned data to a new CSV file
selected_scenario_raw_data.to_csv('cleaned_data.csv', index=False)

# selected_scenario_raw_data.index.set_levels(selected_scenario_raw_data.index.get_level_values(level=1).str.strip()), level = 1, inplace=True)

# print(selected_scenario_raw_data.to_string)
print(selected_scenario_raw_data.index)
print(selected_scenario_raw_data.columns)
# print(selected_scenario_raw_data.loc[selected_scenario_raw_data.index[[1, 2]], 'used model'])

# calc_util.get_vehicle_class(df_data=selected_scenario_raw_data)
# calc_util.show_consumption_manufacturer(df_data=selected_scenario_raw_data)

# start of layout
app.layout = dbc.Container([
    header.header_images,
    html.Div([
        dcc.Dropdown(options=csv_files, id='scenario-dropdown'),
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
            dbc.Table.from_dataframe(id='raw_data_table', df=selected_scenario_raw_data, striped=True, bordered=True,
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
    global selected_scenario_raw_data
    selected_scenario_raw_data = pd.read_csv(f'{folder_path}/{file_name}', sep=';', decimal=",", thousands='.',
                                             encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
    updated_table = dbc.Table.from_dataframe(id='raw_data_table', df=selected_scenario_raw_data, striped=True,
                                             bordered=True, hover=True, index=True)
    return updated_table


if __name__ == '__main__':
    app.run(debug=True)

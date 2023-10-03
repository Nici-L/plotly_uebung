import dash
import dash_bootstrap_components as dbc
import os

import scipy as scipy
from matplotlib import pyplot as plt

import numpy
import pandas as pd
import source.components.Tab_1.layout_header as header
from dash import html, dcc, Output, Input, State, no_update
import config as config
import utils.calculations as calc
import plotly.graph_objects as go
import plotly.express as px
import utils.colors_KIT_plotly as clr
from datetime import datetime


# init app
# todo: grafik aufhübschen, Meldung wenn Werte arg klein sind (Modal Button?) (x-mal kleiner als größter Wert) und man sie deshalb nicht sieht, emission targets ergänzen
# todo: Methoden Beschreibungen verbessern
# todo: LCA ergänzen
# todo: ausgrauen bei dropdown wenn es option nicht gibt
# todo: genaue Zahlen an bars ergänzen
# todo: parameter menu wird noch nicht zurückgesetzt wenn wieder szenario ausgewählt wird
# todo: hover labels für Fahrzeugmodell
# todo:consumption input feld macht keinen sinn

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], assets_url_path='/source/assets')

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

map_colors = {
    ## Vehicles
    "bev": clr.orange_base,
    "hev": clr.maygreen_base,
    "icev": clr.blue2_base,
    "ICEV-g": clr.green1_base,
    "phev": clr.purple_base,
    ## Life cycle phases
    "production": clr.blue2_base,
    "usage": clr.green1_base,
    "recycling": clr.gray_dark25,
    ## Fuels
    "Super E10": clr.green4_dark25,
    "Super E20": clr.green4_base,
    "Super Plus/Super 95": clr.green4_dark50,
    "BtL-Gasoline": clr.green4_bright80,
    "Diesel Premium/Diesel B7": clr.blue5_dark50,
    "PtL-Diesel": clr.blue5_bright80,
    "HVO": clr.cyan_bright80,
}

colors = [
    clr.orange_base,
    clr.maygreen_base,
    clr.blue2_base,
    clr.green1_base,
    clr.purple_base,
    clr.blue5_base,
    clr.gray_base,
]

# initialize global variables
selected_scenario: pd.DataFrame
consumption_per_year_liter: pd.Series
consumption_per_year_kwh: pd.Series
consumption_per_year_liter_with_energy_supply: pd.Series
consumption_per_year_kWh_with_energy_supply: pd.Series
co2e_ttw_per_car: pd.Series
co2e_ttw_per_car_df: pd.DataFrame
co2e_ttw_per_segment: pd.Series
co2e_ttw_per_segment_df: pd.DataFrame
co2e_wtw_per_car: pd.Series
co2e_wtw_per_car_df: pd.DataFrame
co2e_wtw_per_segment: pd.Series
co2e_wtw_per_segment_df: pd.DataFrame
co2e_production_one_car: pd.Series
co2e_savings_one_car: pd.Series


def calculate_variables_based_on_scenario(scenario_df: pd.DataFrame):    # (scenario_name: str):
    # calculating consumption per year
    consumption_per_year_liter = calc.calculate_yearly_consumption_liter(scenario_df)
    consumption_per_year_kwh = calc.calculate_yearly_consumption_kwh(scenario_df)
    # add energy supply column
    consumption_per_year_liter_with_energy_supply = consumption_per_year_liter.to_frame('consumption_manufacturer_l').join(scenario_df['energysupply'])
    consumption_per_year_kWh_with_energy_supply = consumption_per_year_kwh.to_frame('consumption_manufacturer_kWh').join(scenario_df['energysupply'])
    # calculating co2e ttw per year per car
    co2e_ttw_per_car = calc.get_co2e_usage_ttw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, scenario_df)
    co2e_ttw_per_car_df = co2e_ttw_per_car.to_frame('co2e')
    # calculating co2e ttw per year per segment
    co2e_ttw_per_segment = calc.get_co2e_usage_ttw_per_segment(co2e_ttw_per_car, scenario_df)
    co2e_ttw_per_segment_df = co2e_ttw_per_segment.to_frame('co2e')
    # calculating co2e wtw per year per car
    co2e_wtw_per_car = calc.get_co2e_usage_wtw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, scenario_df)
    co2e_wtw_per_car_df = co2e_wtw_per_car.to_frame('co2e')
    # calculating co2e wtw per year per segment
    co2e_wtw_per_segment = calc.get_co2e_usage_wtw_per_segment(co2e_wtw_per_car, scenario_df)
    co2e_wtw_per_segment_df = co2e_wtw_per_segment.to_frame('co2e')
    # calculating co2e of production for one car
    co2e_production_one_car = calc.calculate_production_co2e_per_car(scenario_df)
    # calculate co2e savings (recycling)
    co2e_savings_one_car = calc.calculate_co2e_savings(scenario_df)
    results = {
        "selected_scenario": scenario_df,
        "consumption_per_year_liter": consumption_per_year_liter,
        "consumption_per_year_kwh": consumption_per_year_kwh,
        "consumption_per_year_liter_with_energy_supply": consumption_per_year_liter_with_energy_supply,
        "consumption_per_year_kWh_with_energy_supply": consumption_per_year_kWh_with_energy_supply,
        "co2e_ttw_per_car": co2e_ttw_per_car,
        "co2e_ttw_per_car_df": co2e_ttw_per_car_df,
        "co2e_ttw_per_segment": co2e_ttw_per_segment,
        "co2e_ttw_per_segment_df": co2e_ttw_per_segment_df,
        "co2e_wtw_per_car": co2e_wtw_per_car,
        "co2e_wtw_per_car_df": co2e_wtw_per_car_df,
        "co2e_wtw_per_segment": co2e_wtw_per_segment,
        "co2e_wtw_per_segment_df": co2e_wtw_per_segment_df,
        "co2e_production_one_car": co2e_production_one_car,
        "co2e_savings_one_car": co2e_savings_one_car,
    }
    return results


def init_global_variables(selected_scenario_name: str = None, scenario_df: pd.DataFrame = None):
    global selected_scenario
    if scenario_df is None:
        selected_scenario = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{selected_scenario_name}', sep=';', decimal=",",
                                        thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True,
                                        header=[3])
    else:
        selected_scenario = scenario_df
    calculation_results = calculate_variables_based_on_scenario(selected_scenario)

    # calculating consumption per year
    global consumption_per_year_liter
    consumption_per_year_liter = calculation_results.get("consumption_per_year_liter")
    global consumption_per_year_kwh
    consumption_per_year_kwh = calculation_results.get("consumption_per_year_kwh")
    # add energy supply column
    global consumption_per_year_liter_with_energy_supply
    consumption_per_year_liter_with_energy_supply = calculation_results.get("consumption_per_year_liter_with_energy_supply")
    global consumption_per_year_kWh_with_energy_supply
    consumption_per_year_kWh_with_energy_supply = calculation_results.get("consumption_per_year_kWh_with_energy_supply")
    # calculating co2e ttw per year per car
    global co2e_ttw_per_car
    co2e_ttw_per_car = calculation_results.get("co2e_ttw_per_car")
    global co2e_ttw_per_car_df
    co2e_ttw_per_car_df = calculation_results.get("co2e_ttw_per_car_df")
    # calculating co2e ttw per year per segment
    global co2e_ttw_per_segment
    co2e_ttw_per_segment = calculation_results.get("co2e_ttw_per_segment")
    global co2e_ttw_per_segment_df
    co2e_ttw_per_segment_df = calculation_results.get("co2e_ttw_per_segment_df")
    # calculating co2e wtw per year per car
    global co2e_wtw_per_car
    co2e_wtw_per_car = calculation_results.get("co2e_wtw_per_car")
    global co2e_wtw_per_car_df
    co2e_wtw_per_car_df = calculation_results.get("co2e_wtw_per_car_df")
    # calculating co2e wtw per year per segment
    global co2e_wtw_per_segment
    co2e_wtw_per_segment = calculation_results.get("co2e_wtw_per_segment")
    global co2e_wtw_per_segment_df
    co2e_wtw_per_segment_df = calculation_results.get("co2e_wtw_per_segment_df")
    # calculating co2e of production for one car
    global co2e_production_one_car
    co2e_production_one_car = calculation_results.get("co2e_production_one_car")
    # calculate co2e savings (recycling)
    global co2e_savings_one_car
    co2e_savings_one_car = calculation_results.get("co2e_savings_one_car")


init_global_variables(scenario_filenames[0].get('value'))


def get_fig_sum_total_co2e(co2e_series, dataframe):
    y_icev_sum = co2e_series['icev'].sum()
    y_hev_sum = co2e_series['hev'].sum()
    y_phev_sum = co2e_series['phev'].sum()
    y_bev_sum = co2e_series['bev'].sum()
    fig_sum_total_co2e = go.Figure(data=[
        go.Bar(name='icev', x=['Co<sub>2e</sub> 2022'], y=[y_icev_sum],  marker_color=clr.blue2_base, text=int(y_icev_sum*(10**(-9)))),
        go.Bar(name='hev', x=['Co<sub>2e</sub> 2022'], y=[y_hev_sum], marker_color=clr.maygreen_base),
        go.Bar(name='phev', x=['Co<sub>2e</sub> 2022'], y=[y_phev_sum], marker_color=clr.purple_base),
        go.Bar(name='bev', x=['Co<sub>2e</sub> 2022'], y=[y_bev_sum], marker_color=clr.orange_base)
    ],
            layout={
                'barmode': 'stack',
                'title': 'total CO<sub>2e</sub> emitted by passenger cars <br> per year in kg',
                'plot_bgcolor': '#002b36',  # color Solar stylesheet
                'paper_bgcolor': '#002b36',
                'font_color': 'white'
                }
            )
    print(f"co2 series: {co2e_series}")
    print(f"icev summe:{co2e_series['icev'].sum()}")
    print(f"icev summe:{co2e_series['hev'].sum ()}")
    print(f"icev summe:{co2e_series['phev'].sum ()}")
    print(f"icev summe:{co2e_series['bev'].sum ()}")
    fig_sum_total_co2e.update_yaxes(range=[0, 100000000000], autorange=False)
    fig_sum_total_co2e.update_layout(
        title=dict(text="Total CO<sub>2e</sub> emitted by passenger cars per year in kg", font=dict(size=15, color="lightgray", family="verdana")),
        margin=dict(l=20, r=20, t=80, b=20)
    )
    emission_target_2030 = dataframe['new_emission_targets_germany_2030_fleet'].iloc[0]
    emission_target_2030_only_pkw = emission_target_2030 * 0.68
    fig_sum_total_co2e.add_trace(
        go.Bar(
            x=['Co<sub>2e</sub> target 2030 Germany'],
            y=[emission_target_2030_only_pkw],
            marker_color=clr.green1_base,
            name='target 2030',
            text=int(emission_target_2030_only_pkw*(10**(-9)))
        )
    )
    fig_sum_total_co2e.update_traces(width=0.4)
    # fig_sum_total_co2e.add_annotation(x=['co2e 2022'], y=[y_icev_sum], text="mio t", showarrow=True)

    # fig_sum_total_co2e.update_traces(width=0.5)
    return fig_sum_total_co2e


def get_fig_co2e_segment_all_vehicle_classes(co2e_dataframe, chosen_segment):
    x_val = co2e_dataframe.loc[(slice(None), f"{chosen_segment}"), "co2e"]
    fig_co2e_segment_all_vehicle_classes = px.bar(x_val.to_frame('co2e'), x=x_val.to_frame('co2e').index.get_level_values(0), y='co2e', color_discrete_map=map_colors, text_auto='.2s', color=x_val.to_frame('co2e').index.get_level_values(0))
    fig_co2e_segment_all_vehicle_classes.update_layout(
            title='CO<sub>2e</sub> per segment and drivechain per year in kg',
            yaxis_title="Co<sub>2e</sub> in kg",
            xaxis_title="vehicle class",
            plot_bgcolor='#002b36',  # color Solar stylesheet
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='relative',
            hovermode="x unified")
    # fig_co2e_segment_all_vehicle_classes.update_yaxes(range=[0, 8000000000], autorange=False)
    fig_co2e_segment_all_vehicle_classes.update_traces(width=0.6)
    return fig_co2e_segment_all_vehicle_classes


def get_fig_consumption(co2e_dataframe, chosen_segments, chosen_vehicle_class):
    consumption_segments = co2e_dataframe.loc[(chosen_vehicle_class, chosen_segments), "consumption_manufacturer_l"].to_frame('consumption')
    fig_consumption = px.bar(data_frame=consumption_segments, y=consumption_segments.index.get_level_values(0), x='consumption', orientation='h', barmode='group', color=consumption_segments.index.get_level_values(1), color_discrete_map=map_colors, text_auto='.2s', hover_name = co2e_dataframe.loc[(chosen_vehicle_class, chosen_segments), "used_model"])
    fig_consumption.update_layout(
            title='Fuel consumption per car in liter per 100 km',
            yaxis_title="vehicle class",
            legend_title="segment",
            plot_bgcolor='#002b36',  # color Solar stylesheet
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='group',
    )
    fig_consumption.update_xaxes(range=[0, 30], autorange=False)
    fig_consumption.update_traces(width=0.2)
    return fig_consumption


def get_fig_consumption_kwh(co2e_dataframe, chosen_segments, chosen_vehicle_class):
    consumption_segments = co2e_dataframe.loc[(chosen_vehicle_class, chosen_segments), "consumption_manufacturer_kWh"].to_frame('consumption')
    fig_consumption_kwh = px.bar(data_frame=consumption_segments, y=consumption_segments.index.get_level_values(0), x='consumption', orientation='h', barmode='group', color=consumption_segments.index.get_level_values(1), color_discrete_map=map_colors, text_auto='.2s')
    fig_consumption_kwh.update_layout(
            title='Electricity consumption per car in kWh per 100 km',
            yaxis_title="vehicle class",
            legend_title="segment",
            plot_bgcolor='#002b36',  # color Solar stylesheet
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='group',
    )
    fig_consumption_kwh.update_xaxes(range=[0, 25], autorange=False)
    return fig_consumption_kwh


def get_fig_lca_waterfall(chosen_scenario_name, chosen_lca, chosen_vehicle_class, chosen_segment, is_recycling_displayed):
    chosen_scenario_df = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{chosen_scenario_name}', sep=';', decimal=",",
                                     thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True,
                                     header=[3])
    scenario_var = calculate_variables_based_on_scenario(chosen_scenario_df)
    co2e_per_single_car_usage = scenario_var[f"co2e_{chosen_lca}_per_car"].to_frame('co2e')
    co2e_per_single_car_production = scenario_var['co2e_production_one_car'].to_frame('co2e')
    co2e_per_single_car_savings = scenario_var['co2e_savings_one_car'].to_frame('co2e')
    y_value = []
    x_value = []
    measure = []
    print(f"is_recycling_displayed: {type(is_recycling_displayed)}")
    if is_recycling_displayed is True:
        print("is_recycling_displayed is True")
        co2e_per_single_car_total = co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_savings.loc[(chosen_vehicle_class, chosen_segment), 'co2e']
        y_value = [co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_savings.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_total]
        x_value = ["production", "usage", "recycling", "total co2e"]
        measure = ["relative", "relative", "relative", "total"]
    elif is_recycling_displayed is False:
        print("is_recycling_displayed is False")
        co2e_per_single_car_total = co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e']
        y_value = [co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_total]
        x_value = ["production", "usage", "total co2e"]
        measure = ["relative", "relative", "total"]
    else:
        print("nix!")
        co2e_per_single_car_total = co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_savings.loc[(chosen_vehicle_class, chosen_segment), 'co2e']
        y_value = [co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_savings.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_total]
        x_value = ["production", "usage", "recycling", "total co2e"]
        measure = ["relative", "relative", "relative", "total"]

    fig_lca_waterfall = go.Figure(go.Waterfall(
        name="lca values", orientation="v",
        measure=measure,
        x=x_value,
        textposition="outside",
        text=["", "", "", ""],
        y=y_value,
        connector={"line": {"color": 'rgba(0,150,130,1)'}},
        decreasing={"marker": {"color": clr.gray_dark25, "line": {"color": "grey", "width": 2}}},
        increasing={"marker": {"color": clr.blue2_base, "line": {"color": "rgba(140,161,208,1)", "width": 2}}},
        totals={"marker": {"color": clr.green1_base, "line": {"color": "rgba(0,113,98,1)", "width": 3}}}
    ))
    fig_lca_waterfall.update_layout(
        title="LCA of a single car",
        showlegend=True,
        plot_bgcolor='#002b36',  # color Solar stylesheet
        paper_bgcolor='#002b36',
        font_color='white'
    )
    return fig_lca_waterfall


def calc_quadratic_regression(x, y, x_new):
    plt.plot(x, y)
    plt.show()

    # polynom approximation
    [a, b, c] = numpy.polyfit(x=x, y=y, deg=2)

    print(f"a: {a}, b: {b}, c: {c}")
    print(f"x : {x}")
    print(f"y : {y}")
    print(f"x_new : {x_new}")
    y_new = a * x_new[:] ** 2 + b * x_new[:] + c
    plt.plot(x_new, y_new)
    plt.show()
    # polynom approximation
    # vectorized calculation for entire array
    return y_new


def get_yearly_co2_fig(regression_array, x_array):
    yearly_co2e_fig = go.Figure([go.Bar(x=x_array, y=regression_array, marker_color=clr.green1_base)])
    yearly_co2e_fig.update_layout(
        title='Co<sub>2e</sub> of passenger cars in Germany from 1990 until 2050',
        yaxis_title="co2e in kg",
        xaxis_title="",
        plot_bgcolor='#002b36',  # color Solar stylesheet
        paper_bgcolor='#002b36',
        font_color='white',
        barmode='relative',
        hovermode="x unified")
    return yearly_co2e_fig


x_since_1990 = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
y_since_1990 = [110000000000, 112200000000, 116280000000, 119000000000, 116280000000, 119000000000, 119000000000, 119000000000, 121000000000, 125000000000, 123000000000, 120000000000, 119000000000, 114920000000, 114240000000, 108000000000, 106000000000, 104000000000, 104000000000, 104000000000, 104000000000, 104000000000, 104000000000,107440000000, 108000000000,109000000000, 111000000000,113000000000,110000000000]
x = numpy.array([2019, 2030, 2045])
y = numpy.array([111520000000, selected_scenario['co2e_2030'].iloc[0], selected_scenario['co2e_2045'].iloc[0]])
x_new = numpy.arange(2019, 2050, 1)
x_array_combined = numpy.concatenate((x_since_1990, x_new))
print(f"x array {x_array_combined}")

yearly_co2e_regression = calc_quadratic_regression(x=x, y=y, x_new=x_new)

y_array_combined = numpy.concatenate((y_since_1990, yearly_co2e_regression))
print(f"y combined{y_array_combined}")


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
                           dbc.Button(['share of E5 on total gasoline',
                                       dbc.Badge("%", color="light", text_color="primary", className="ms-1")],
                                      id='share_E5_totalgasoline_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="share_E5", type="number", placeholder="share E5", min=0, max=100, step=1, style={'marginRight':'10px'}, value=90),

                           dbc.Button(['share of E10 on total gasoline',
                                       dbc.Badge("%", color="light", text_color="primary", className="ms-1")],
                                      id='share_E10_totalgasoline_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="share_E10", type="number", placeholder="share E10", min=0, max=100, step=1, style={'marginRight': '10px'}, value=10),

                           dbc.Button(['share of diesel',
                                       dbc.Badge("%", color="light", text_color="primary", className="ms-1")],
                                      id='share_diesel_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="share_diesel", type="number", placeholder="share diesel", min=0, max=100, step=1, style={'marginRight': '10px'}, value=100),

                           dbc.Button(['co2e emitted during production of electricity',
                                       dbc.Badge("g/kWh", color="light", text_color="primary", className="ms-1")],
                                      id='co2e_electricity_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="co2e_electricity", type="number", placeholder="co2e electricity", min=0, max=1000, step=0.1, style={'marginRight': '10px'}, value=400),

                           dbc.Button(['vehicle stock',
                                       dbc.Badge("mio", color="light", text_color="primary", className="ms-1")],
                                      id='vehicle_stock_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="vehicle_stock", type="number", placeholder="vehicle stock", min=1, max=50000000, step=1, style={'marginRight': '10px'}, value=48),

                           dbc.Button(['share icev',
                                       dbc.Badge("%", color="light", text_color="primary", className="ms-1")],
                                      id='share_icev_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="share_icev", type="number", placeholder="share icev", min=0, max=100, step=1, style={'marginRight': '10px'}, value=70),

                           dbc.Button(['share hev',
                                       dbc.Badge("%", color="light", text_color="primary", className="ms-1")],
                                      id='share_hev_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="share_hev", type="number", placeholder="share hev", min=0, max=100, step=1, style={'marginRight': '10px'}, value=10),

                           dbc.Button(['share phev',
                                       dbc.Badge("%", color="light", text_color="primary", className="ms-1")],
                                      id='share_phev_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="share_phev", type="number", placeholder="share phev", min=0, max=100, step=1, style={'marginRight': '10px'}, value=10),

                           dbc.Button(['share bev',
                                       dbc.Badge("%", color="light", text_color="primary", className="ms-1")],
                                      id='share_bev_button', n_clicks=0, color='primary', class_name='button m-2'),
                           dcc.Input(id="share_bev", type="number", placeholder="share_bev", min=0, max=100, step=1, style={'marginRight': '10px'}, value=10),

                           html.Div([
                               dbc.Button(id='calculate-button', n_clicks=0, children='calculate', color='success', size='lg', class_name='m-3 calculate-button')
                           ]),
                           # dbc.Button(id='glider_weight-button', n_clicks=0, children='glider_weight', color='primary', class_name='m-2'),
                           # dbc.Button(id='co2e_production-button', n_clicks=0, children='co2e_production', color='primary', class_name='m-2'),
                           # dbc.Button(id='battery_capacity_brutto-button', n_clicks=0, children='battery_capacity_brutto', color='primary', class_name='m-2'),
                           # dbc.Button(id='co2e_battery_production-button', n_clicks=0, children='co2e_battery_production', color='primary', class_name='m-2'),
                           # dbc.Button(id='co2e_savings_glider-button', n_clicks=0, children='co2e_savings_glider', color='primary', class_name='m-2'),
                           # dbc.Button(id='co2e_savings_battery-button', n_clicks=0, children='co2e_savings_battery', color='primary', class_name='m-2'),
                           # dbc.Button(id='co2e_E5_TtW-button', n_clicks=0, children='co2e_E5_TtW', color='primary', class_name='m-2'),
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
                    dcc.Graph(id='co2e_ttw_barchart', figure=get_fig_sum_total_co2e(co2e_ttw_per_segment, selected_scenario), className='mt-5'),
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
                        dbc.Card(dbc.CardBody("The Co2e emissions of Germany are defined by the government. This offiial number was taken and multiplied with 68% which is the share passenger cars hold on total Co2e emissions caused by traffic.")),
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
                    dcc.Dropdown(options=selected_scenario.index.get_level_values(1).unique(), id='choose-segments', value='Mini', searchable=False, className='Dropdown-2'),
                    dcc.Dropdown(options=['one car', 'all vehicles'], id='one_car_dropdown', value='all vehicles', className='Dropdown-2'),
                    dcc.Dropdown(options=['TtW', 'WtW'], id='TtW_vehicle_class_fig', value='TtW', className='Dropdown-2'),
                    dcc.Graph(id='co2e_ttw_barchart_car', figure=get_fig_co2e_segment_all_vehicle_classes(co2e_ttw_per_segment_df, 'Kleinwagen'), className='mt-4')
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
                        dbc.Card(dbc.CardBody(
                            "Data: Kraftfahrbundesamt")),
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
                        dcc.Dropdown(options=selected_scenario.index.get_level_values(0).unique(), id='consumption-vehicle-class', multi=True, value=['icev'], className='Dropdown-2'),
                        dcc.Dropdown(options=selected_scenario.index.get_level_values(1).unique(), id='consumption-segment', multi=True, value=['Mini', 'Kleinwagen'], className='Dropdown-2'),
                        dcc.Graph(id='fig-consumption', figure=get_fig_consumption(selected_scenario, ['Mini', 'Kleinwagen'], 'icev')),
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
                  dcc.Dropdown(options=selected_scenario.index.get_level_values(0).unique(), id='lca-vehicle-class', value='icev', className='Dropdown-2'),
                  dcc.Dropdown(options=selected_scenario.index.get_level_values(1).unique(), id='lca-segment', value='Mini', className='Dropdown-2'),
                  dbc.Switch(label='Include recycling', value=True, id='recycling-option', className='recycling_toggle_switch'),
                  dbc.Button(id='selection-button', n_clicks=0, children='apply selection', color='success', size='m', class_name='m-3 selection-button'),
                  dcc.Graph(id='lca-waterfall-fig', figure=get_fig_lca_waterfall(scenario_filenames[0].get('value'), chosen_lca='ttw', chosen_vehicle_class='icev', chosen_segment='Mini', is_recycling_displayed=True))
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
            dcc.Graph(id='co2e_over-the_years_fig', figure=get_yearly_co2_fig(regression_array=y_array_combined, x_array=x_array_combined))
        ])
    ])
])


# callback for scenario dropdown
@app.callback(
    Output(component_id='output_input_div', component_property='children', allow_duplicate=True),
    Input(component_id='scenario-dropdown', component_property='value'),
    prevent_initial_call=True
)
def update_scenario_selection(scenario_chosen):
    init_global_variables(selected_scenario_name=scenario_chosen)
    return f'You have selected: {scenario_chosen} at {datetime.now().strftime("%d.%m.%y %H:%M:%S")}'


# callback for parameter menu accordion
@app.callback(
    Output(component_id='output_input_div', component_property='children', allow_duplicate=True),
    Input(component_id='calculate-button', component_property='n_clicks'),
    [# State(component_id='input_consumption', component_property='value'),
     State(component_id='share_E5', component_property='value'),
     State(component_id='share_E10', component_property='value'),
     State(component_id='share_diesel', component_property='value'),
     State(component_id='co2e_electricity', component_property='value'),
     State(component_id='vehicle_stock', component_property='value'),
     State(component_id='share_icev', component_property='value'),
     State(component_id='share_hev', component_property='value'),
     State(component_id='share_phev', component_property='value'),
     State(component_id='share_bev', component_property='value'),
    ],
    prevent_initial_call=True
)
def update_graph(n, share_E5, share_E10, share_diesel, co2e_electricity, vehicle_stock, share_icev, share_hev, share_phev, share_bev):
    share_hev = share_hev/100
    share_icev = share_icev/100
    share_phev = share_phev/100
    share_bev = share_bev/100
    share_diesel = share_diesel/100
    share_E5 = share_E5/100
    share_E10 = share_E10/100
    vehicle_stock = vehicle_stock*1000000
    co2e_electricity = co2e_electricity/1000
    vehicle_classes_list_without_lkw = list(dict.fromkeys(selected_scenario.index.get_level_values(0).to_list()))
    vehicle_classes_list_without_lkw.remove('lkw')
    # selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'consumption_manufacturer_l'] = consumption
    selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'] = share_E5
    selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'] = share_E10
    selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'] = share_diesel
    selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'] = co2e_electricity
    selected_scenario['vehicle_stock'] = selected_scenario['shareontotalvehicles'] * vehicle_stock
    selected_scenario.loc[('icev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_icev) * selected_scenario.loc[('icev', slice(None)), 'shareontotalvehicles']
    selected_scenario.loc[('hev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_hev) * selected_scenario.loc[('hev', slice(None)), 'shareontotalvehicles']
    selected_scenario.loc[('phev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_phev) * selected_scenario.loc[('phev', slice(None)), 'shareontotalvehicles']
    selected_scenario.loc[('bev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_bev) * selected_scenario.loc[('bev', slice(None)), 'shareontotalvehicles']

    init_global_variables(selected_scenario_name=None, scenario_df=selected_scenario)

    return f'you have selected your own custom scenario at {datetime.now().strftime("%d.%m.%y %H:%M:%S")}'


# callback for TtW or WtW button
@app.callback(
    Output("co2e_ttw_barchart", "figure"),
    [Input("display_figure", "value"),
     Input(component_id='output_input_div', component_property='children')],
    prevent_initital_call=True
)
def update_total_co2e_graph(display_figure, input):
    print(input)

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
     Input('choose-segments', 'value'),
     Input('one_car_dropdown', 'value'),
     Input(component_id='output_input_div', component_property='children')],
)
def update_car_graph(chosen_lc_step, chosen_segment, car_number, input):
    if chosen_lc_step == 'TtW' and car_number == 'all vehicles':
        fig_co2e_segment_all_vehicle_classes = get_fig_co2e_segment_all_vehicle_classes(co2e_ttw_per_segment_df, chosen_segment)
        return fig_co2e_segment_all_vehicle_classes
    elif chosen_lc_step == 'WtW' and car_number == 'all vehicles':
        fig_co2e_segment_all_vehicle_classes = get_fig_co2e_segment_all_vehicle_classes(co2e_wtw_per_segment_df, chosen_segment)
        return fig_co2e_segment_all_vehicle_classes
    elif chosen_lc_step == 'TtW' and car_number == 'one car':
        fig_co2e_segment_all_vehicle_classes = get_fig_co2e_segment_all_vehicle_classes(co2e_ttw_per_car_df, chosen_segment)
        return fig_co2e_segment_all_vehicle_classes
    elif chosen_lc_step == 'WtW' and car_number == 'one car':
        fig_co2e_segment_all_vehicle_classes = get_fig_co2e_segment_all_vehicle_classes(co2e_wtw_per_car_df, chosen_segment)
        return fig_co2e_segment_all_vehicle_classes
    else:
        fig_co2e_segment_all_vehicle_classes = {}
    return fig_co2e_segment_all_vehicle_classes


# callback for segment and vehicle class dropdown
@app.callback(
    Output('fig-consumption', 'figure'),
    [Input('kWh-or-liter', 'value'),
     Input('consumption-segment', 'value'),
     Input('consumption-vehicle-class', 'value'),
     Input(component_id='output_input_div', component_property='children')],
    prevent_initial_call=True
)
def update_consumption_graph(chosen_unit, chosen_segments, chosen_vehicle_class, input):
    if chosen_unit == 'liter' and chosen_vehicle_class is None or len(chosen_vehicle_class) == 0 and chosen_segments is None or len(chosen_segments) == 0 or None:
        return no_update
    elif chosen_unit == 'liter' and len(chosen_vehicle_class) == 0 and len(chosen_segments) == 1:
        fig_consumption = get_fig_consumption(selected_scenario, chosen_segments, slice(None))
        return fig_consumption
    elif chosen_unit == 'liter' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) == 1:
        fig_consumption = get_fig_consumption(selected_scenario, chosen_segments, chosen_vehicle_class)
        return fig_consumption
    elif chosen_unit == 'liter' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) >= 1:
        fig_consumption = get_fig_consumption(selected_scenario, chosen_segments, chosen_vehicle_class)
        return fig_consumption

    elif chosen_unit == 'kWh' and chosen_vehicle_class is None or len(chosen_vehicle_class) == 0 and chosen_segments is None or len(chosen_segments) == 0 or None:
        return no_update
    elif chosen_unit == 'kWh' and len(chosen_vehicle_class) == 0 and len(chosen_segments) == 1:
        fig_consumption = get_fig_consumption_kwh(selected_scenario, chosen_segments, slice(None))
        return fig_consumption
    elif chosen_unit == 'kWh' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) == 1:
        fig_consumption = get_fig_consumption_kwh(selected_scenario, chosen_segments, chosen_vehicle_class)
        return fig_consumption
    elif chosen_unit == 'kWh' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) >= 1:
        fig_consumption = get_fig_consumption_kwh(selected_scenario, chosen_segments, chosen_vehicle_class)
        return fig_consumption
    else:
        return no_update


# callback for scenario comparison
@app.callback(
    Output('scenario-comparison', 'figure'),
    [Input('scenario-dropdown-comparison', 'value'),
     Input('chose_lca_comparison_fig', 'value'),
     Input(component_id='details-toggle-option', component_property='value')],
    prevent_initital_call=True
)
def update_comparison_graph(chosen_scenario_list, chosen_unit, show_details):
    chosen_unit = str(chosen_unit).lower()
    if not type(chosen_scenario_list) == list:
        chosen_scenario_list = [chosen_scenario_list]
    fig_comparison = go.Figure()
    for scenario_name in chosen_scenario_list:
        current_scenario_df = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{scenario_name}', sep=';', decimal=",", thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
        scenario_var = calculate_variables_based_on_scenario(current_scenario_df)
        fig_comparison.add_trace(
            go.Bar(
                y=[str(scenario_name).replace('_', ' ').replace('.CSV', '').replace('.csv', '')],
                x=[scenario_var[f"co2e_{chosen_unit}_per_segment"].sum()],
                orientation='h',
                marker_color=clr.green1_base,
            )
        )
        fig_comparison.update_layout(
            title='Comparison between different scenarios',
            legend_title_text="LCA",
            plot_bgcolor='#002b36',  # color Solar stylesheet
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='group',
            autosize=True,
            showlegend=False,
        )
        fig_comparison.update_yaxes(title_text="Scenarios")
        fig_comparison.update_xaxes(range=[0, 100000000000], autorange=False)
        fig_comparison.update_traces(width=0.5)
    return fig_comparison


@app.callback(
    Output('lca-waterfall-fig', 'figure'),
    Input(component_id='output_input_div', component_property='children'),
    Input(component_id='selection-button', component_property='n_clicks'),
    Input(component_id='recycling-option', component_property='value'),
    State('scenario-dropdown-lca', 'value'),
    State('chose_lca', 'value'),
    State('lca-vehicle-class', 'value'),
    State('lca-segment', 'value'),

)
def update_waterfall_lca_graph(scenario_selection, n, is_recycling_displayed, chosen_scenario, chosen_lca, chosen_vehicle_class, chosen_segment):
    chosen_lca = str(chosen_lca).lower()
    print(f"is_recycling_displayed: {is_recycling_displayed}")
    fig_lca_waterfall = get_fig_lca_waterfall(chosen_scenario_name=chosen_scenario, chosen_lca=chosen_lca, chosen_vehicle_class=chosen_vehicle_class, chosen_segment=chosen_segment, is_recycling_displayed=is_recycling_displayed)
    return fig_lca_waterfall


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button-1", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse 2", "is_open"),
    [Input("collapse-button-2", "n_clicks")],
    [State("collapse 2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse 3", "is_open"),
    [Input("collapse-button-3", "n_clicks")],
    [State("collapse 3", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse 4", "is_open"),
    [Input("collapse-button-4", "n_clicks")],
    [State("collapse 4", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse 5", "is_open"),
    [Input("collapse-button-5", "n_clicks")],
    [State("collapse 5", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("modal-xl", "is_open"),
    Input("open-xl", "n_clicks"),
    State("modal-xl", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run(debug=True)

# todo:  https://dash.plotly.com/background-callbacks#:~:text=debug%3DTrue)-,Example%202%3A%20Disable%20Button%20While%20Callback%20Is%20Running,-Notice%20how%20in
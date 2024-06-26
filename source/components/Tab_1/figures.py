
import plotly.graph_objects as go
import plotly.express as px
import source.utils.colors_KIT_plotly as clr
import pandas as pd
import source.utils.calculations as calc
import source.config as config
import numpy
import os
import numpy as np


scenario_filenames = []
for file in os.listdir(config.SCENARIO_FOLDER_PATH):
    if file.endswith('.CSV') or file.endswith('.csv'):
        # scenario_filenames.append(file)
        scenario_filenames.append({
            'value': file,
            'label': file.replace('_', ' ').replace('.CSV', '').replace('.csv', ''),
        })
print(f"scenario_filenames: {scenario_filenames}")
print(f"figures.py:{os.listdir(config.SCENARIO_FOLDER_PATH)}")


# type hint global variables (simplifies code completion)
selected_scenario: pd.DataFrame
consumption_per_year_liter: pd.Series
consumption_per_year_kwh: pd.Series
consumption_per_km_liter: pd.Series
consumption_per_km_kwh: pd.Series
consumption_per_year_liter_with_energy_supply: pd.Series
consumption_per_year_kWh_with_energy_supply: pd.Series
consumption_per_km_liter_with_energy_supply: pd.Series
consumption_per_km_kwh_with_energy_supply: pd.Series
co2e_ttw_per_car_per_km: pd.Series
co2e_ttw_per_car: pd.Series
co2e_ttw_per_car_df: pd.DataFrame
co2e_ttw_per_segment: pd.Series
co2e_ttw_per_segment_df: pd.DataFrame
co2e_wtw_per_car_per_km: pd.Series
co2e_wtw_per_car: pd.Series
co2e_wtw_per_car_df: pd.DataFrame
co2e_wtw_per_segment: pd.Series
co2e_wtw_per_segment_df: pd.DataFrame
co2e_production_one_car: pd.Series
co2e_production_per_vehicle_class_all: pd.Series
co2e_savings_one_car: pd.Series
unique_dict_values: list

# color solar stylesheet: #002b36
map_colors = {
    ## Vehicles
    "BEV": clr.orange_base,
    "HEV": clr.maygreen_base,
    "ICEV": clr.blue2_base,
    "ICEV-g": clr.green1_base,
    "PHEV": clr.purple_base,
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


def calculate_variables_based_on_scenario(scenario_df: pd.DataFrame):    # (scenario_name: str):
    """
    Calculate various variables based on a given scenario represented as a DataFrame.

    :param scenario_df: A DataFrame containing data for the scenario.
    :type scenario_df: pd.DataFrame

    :return: A dictionary containing the following calculated variables:
        - "selected_scenario": The input scenario DataFrame.
        - "consumption_per_year_liter": Yearly consumption in liters.
        - "consumption_per_year_kwh": Yearly consumption in kilowatt-hours.
        - "consumption_per_year_liter_with_energy_supply": Yearly consumption in liters with energy supply data.
        - "consumption_per_year_kWh_with_energy_supply": Yearly consumption in kilowatt-hours with energy supply data.
        - "co2e_ttw_per_car": CO2 equivalent emissions per car for the scenario.
        - "co2e_ttw_per_car_df": DataFrame of CO2 equivalent emissions per car.
        - "co2e_ttw_per_segment": CO2 equivalent emissions per segment for the scenario.
        - "co2e_ttw_per_segment_df": DataFrame of CO2 equivalent emissions per segment.
        - "co2e_wtw_per_car": CO2 equivalent emissions per car for well-to-wheel analysis.
        - "co2e_wtw_per_car_df": DataFrame of CO2 equivalent emissions per car for well-to-wheel.
        - "co2e_wtw_per_segment": CO2 equivalent emissions per segment for well-to-wheel analysis.
        - "co2e_wtw_per_segment_df": DataFrame of CO2 equivalent emissions per segment for well-to-wheel.
        - "co2e_production_one_car": CO2 equivalent emissions for the production of one car.
        - "co2e_savings_one_car": CO2 equivalent emissions savings through recycling.
    :rtype: dict

    The function calculates and compiles these variables and returns them in a dictionary.
    """

    # calculating consumption per year
    consumption_per_year_liter = calc.calculate_yearly_consumption_liter(scenario_df.copy())
    consumption_per_year_kwh = calc.calculate_yearly_consumption_kwh(scenario_df.copy())
    # calculating consumption per km
    consumption_per_km_liter = calc.calculate_consumption_liter_per_km(scenario_df.copy())
    consumption_per_km_kwh = calc.calculate_consumption_kwh_per_km(scenario_df.copy())
    # add energy supply column
    consumption_per_km_liter_with_energy_supply = consumption_per_km_liter.to_frame('consumption_manufacturer_l').join(scenario_df['energysupply'])
    consumption_per_km_kwh_with_energy_supply = consumption_per_km_kwh.to_frame('consumption_manufacturer_kWh').join(scenario_df['energysupply'])
    # add energy supply column
    consumption_per_year_liter_with_energy_supply = consumption_per_year_liter.to_frame('consumption_manufacturer_l').join(scenario_df['energysupply'])
    consumption_per_year_kWh_with_energy_supply = consumption_per_year_kwh.to_frame('consumption_manufacturer_kWh').join(scenario_df['energysupply'])
    # calculating co2 ttw per km per car
    co2e_ttw_per_car_per_km = calc.get_co2e_usage_ttw_per_car_per_km(consumption_per_km_liter_with_energy_supply, consumption_per_km_kwh_with_energy_supply, scenario_df.copy())
    # calculating co2e ttw per year per car
    co2e_ttw_per_car = calc.get_co2e_usage_ttw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, scenario_df.copy())
    co2e_ttw_per_car_df = co2e_ttw_per_car.to_frame('co2e')
    # calculating co2e ttw per year per segment
    co2e_ttw_per_segment = calc.get_co2e_usage_ttw_per_segment(co2e_ttw_per_car, scenario_df.copy())
    co2e_ttw_per_segment_df = co2e_ttw_per_segment.to_frame('co2e')
    # calculating co2e wtw per km per car
    co2e_wtw_per_car_per_km = calc.get_co2e_usage_wtw_per_car_per_km(consumption_per_km_liter_with_energy_supply, consumption_per_km_kwh_with_energy_supply, scenario_df.copy())
    # calculating co2e wtw per year per car
    co2e_wtw_per_car = calc.get_co2e_usage_wtw_per_car(consumption_per_year_liter_with_energy_supply, consumption_per_year_kWh_with_energy_supply, scenario_df.copy())
    co2e_wtw_per_car_df = co2e_wtw_per_car.to_frame('co2e')
    # calculating co2e wtw per year per segment
    co2e_wtw_per_segment = calc.get_co2e_usage_wtw_per_segment(co2e_wtw_per_car, scenario_df.copy())
    co2e_wtw_per_segment_df = co2e_wtw_per_segment.to_frame('co2e')
    # calculating co2e of production for one car
    co2e_production_one_car = calc.calculate_production_co2e_per_car(scenario_df.copy())
    # calculating co2e of production for whole vehicle class
    co2e_production_per_vehicle_class_all = calc.calculate_production_co2e_per_vehicle_class(co2e_production_one_car, scenario_df.copy())
    # calculate co2e savings (recycling)
    co2e_savings_one_car = calc.calculate_co2e_savings(scenario_df.copy())
    # dictionary for return variables to save variables but not write them into global variables
    results = {
        "selected_scenario": scenario_df.copy(),
        "consumption_per_year_liter": consumption_per_year_liter,
        "consumption_per_year_kwh": consumption_per_year_kwh,
        "consumption_per_km_liter": consumption_per_km_liter,
        "consumption_per_km_kwh": consumption_per_km_kwh,
        "consumption_per_km_liter_with_energy_supply": consumption_per_km_liter_with_energy_supply,
        "consumption_per_km_kwh_with_energy_supply": consumption_per_km_kwh_with_energy_supply,
        "consumption_per_year_liter_with_energy_supply": consumption_per_year_liter_with_energy_supply,
        "consumption_per_year_kWh_with_energy_supply": consumption_per_year_kWh_with_energy_supply,
        "co2e_ttw_per_car_per_km": co2e_ttw_per_car_per_km,
        "co2e_ttw_per_car": co2e_ttw_per_car,
        "co2e_ttw_per_car_df": co2e_ttw_per_car_df,
        "co2e_ttw_per_segment": co2e_ttw_per_segment,
        "co2e_ttw_per_segment_df": co2e_ttw_per_segment_df,
        "co2e_wtw_per_car_per_km": co2e_wtw_per_car_per_km,
        "co2e_wtw_per_car": co2e_wtw_per_car,
        "co2e_wtw_per_car_df": co2e_wtw_per_car_df,
        "co2e_wtw_per_segment": co2e_wtw_per_segment,
        "co2e_wtw_per_segment_df": co2e_wtw_per_segment_df,
        "co2e_production_one_car": co2e_production_one_car,
        "co2e_savings_one_car": co2e_savings_one_car,
        "co2e_production_per_vehicle_class_all": co2e_production_per_vehicle_class_all,
    }
    #print(f"results aus Methode:{results}")
    return results


# function overwrites global variables
def init_global_variables(selected_scenario_name: str = None, scenario_df: pd.DataFrame = None):
    """
     Initialize global variables based on the selected scenario and calculation results.

     :param selected_scenario_name: The name of the selected scenario (file name).
     :type selected_scenario_name: str

     :param scenario_df: A pandas DataFrame containing scenario data (optional if selected_scenario_name is provided).
     :type scenario_df: pd.DataFrame

     This function initializes the following global variables based on the selected scenario and calculation results:

     - global selected_scenario: The selected scenario DataFrame.
     - global consumption_per_year_liter: Yearly consumption in liters.
     - global consumption_per_year_kwh: Yearly consumption in kilowatt-hours.
     - global consumption_per_year_liter_with_energy_supply: Yearly consumption in liters with energy supply data.
     - global consumption_per_year_kWh_with_energy_supply: Yearly consumption in kilowatt-hours with energy supply data.
     - global co2e_ttw_per_car: CO2 equivalent emissions per car for the scenario.
     - global co2e_ttw_per_car_df: DataFrame of CO2 equivalent emissions per car.
     - global co2e_ttw_per_segment: CO2 equivalent emissions per segment for the scenario.
     - global co2e_ttw_per_segment_df: DataFrame of CO2 equivalent emissions per segment.
     - global co2e_wtw_per_car: CO2 equivalent emissions per car for well-to-wheel analysis.
     - global co2e_wtw_per_car_df: DataFrame of CO2 equivalent emissions per car for well-to-wheel.
     - global co2e_wtw_per_segment: CO2 equivalent emissions per segment for well-to-wheel analysis.
     - global co2e_wtw_per_segment_df: DataFrame of CO2 equivalent emissions per segment for well-to-wheel.
     - global co2e_production_one_car: CO2 equivalent emissions for the production of one car.
     - global co2e_savings_one_car: CO2 equivalent emissions savings through recycling.
     """
    global selected_scenario
    if scenario_df is None:
        selected_scenario = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{selected_scenario_name}', sep=';', decimal=",",
                                        thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True,
                                        header=[5])
    else:
        selected_scenario = scenario_df.copy()
        # print(f"selected scenario init methode:{selected_scenario.to_string()} {time.time()}")
    calculation_results = calculate_variables_based_on_scenario(selected_scenario.copy())

    # calculating consumption per year
    global consumption_per_year_liter
    consumption_per_year_liter = calculation_results.get("consumption_per_year_liter")
    global consumption_per_year_kwh
    consumption_per_year_kwh = calculation_results.get("consumption_per_year_kwh")
    # calculating consumption per km
    global consumption_per_km_liter
    consumption_per_km_liter = calculation_results.get("consumption_per_km_liter")
    global consumption_per_km_kwh
    consumption_per_km_kwh = calculation_results.get("consumption_per_km_kwh")
    # add energy supply column
    global consumption_per_km_liter_with_energy_supply
    consumption_per_km_liter_with_energy_supply = calculation_results.get("consumption_per_km_liter_with_energy_supply")
    global consumption_per_km_kwh_with_energy_supply
    consumption_per_km_kwh_with_energy_supply = calculation_results.get("consumption_per_km_kwh_with_energy_supply")
    # add energy supply column
    global consumption_per_year_liter_with_energy_supply
    consumption_per_year_liter_with_energy_supply = calculation_results.get("consumption_per_year_liter_with_energy_supply")
    global consumption_per_year_kWh_with_energy_supply
    consumption_per_year_kWh_with_energy_supply = calculation_results.get("consumption_per_year_kWh_with_energy_supply")
    # calculating co2e ttw per km per car
    global co2e_ttw_per_car_per_km
    co2e_ttw_per_car_per_km = calculation_results.get("co2e_ttw_per_car_per_km")
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
    # calculating co2e wtw per km per car
    global co2e_wtw_per_car_per_km
    co2e_wtw_per_car_per_km = calculation_results.get("co2e_wtw_per_car_per_km")
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
    # calculate co2e of production for all vehicle classes
    global co2e_production_per_vehicle_class_all
    co2e_production_per_vehicle_class_all = calculation_results.get("co2e_production_per_vehicle_class_all")
    # calculate co2e savings (recycling)
    global co2e_savings_one_car
    co2e_savings_one_car = calculation_results.get("co2e_savings_one_car")


# init_global_variables(scenario_filenames[0].get('value'))


def get_fig_sum_total_co2e(co2e_ttw_series, selected_scenario_df):
    """
        Create a Plotly figure representing the total CO2 emissions for different vehicle classes.

        This function takes a series of CO2 emissions per vehicle class and a DataFrame containing information about
        emission targets for specific years. It generates a Plotly bar chart visualizing the total CO2 emissions for
        ICEV, HEV, PHEV, and BEV, along with emission targets for 2030 and 2040.

        :param Dict[str, Any] co2e_ttw_series:
            A dictionary containing CO2 emissions per vehicle class.

        :param pd.DataFrame selected_scenario_df:
            A Pandas DataFrame containing information about emission targets for specific years.

        :return: go.Figure
            A Plotly figure representing the total CO2 emissions for different vehicle classes and emission targets.
        """
    y_icev_sum = co2e_ttw_series['ICEV'].sum()
    y_hev_sum = co2e_ttw_series['HEV'].sum()
    y_phev_sum = co2e_ttw_series['PHEV'].sum()
    y_bev_sum = co2e_ttw_series['BEV'].sum()
    y_vehicle_sum = y_hev_sum + y_bev_sum + y_phev_sum + y_icev_sum
    vehicles_sum = {'icev_sum': int(y_icev_sum), 'hev_sum': int(y_hev_sum), 'phev_sum': int(y_phev_sum), 'bev_sum': int(y_bev_sum)}
    df_vehicles_sum = pd.DataFrame(data=vehicles_sum, index=['co2e'])
    # print(df_vehicles_sum)
    # print(df_vehicles_sum['icev_sum']['co2e'])
    fig_sum_total_co2e = go.Figure(
        go.Bar(name='ICEV', x=['CO<sub>2e</sub> of <br> chosen scenario'], y=[df_vehicles_sum['icev_sum']['co2e']], marker_color=clr.blue2_base)
    )
    fig_sum_total_co2e.add_trace(
        go.Bar(name='HEV', x=['CO<sub>2e</sub> of <br> chosen scenario'], y=[df_vehicles_sum['hev_sum']['co2e']], marker_color=clr.maygreen_base)
    )
    fig_sum_total_co2e.add_trace(
       go.Bar(name='PHEV', x=['CO<sub>2e</sub> of <br> chosen scenario'], y=[df_vehicles_sum['phev_sum']['co2e']], marker_color=clr.purple_base)
    )
    fig_sum_total_co2e.add_trace(
        go.Bar(name='BEV', x=['CO<sub>2e</sub> of <br> chosen scenario'],
               y=[df_vehicles_sum['bev_sum']['co2e']],
               marker_color=clr.orange_base,
               text=['{:.1f}B'.format(int(y_vehicle_sum) / 1000000000)]
               )
    )
    fig_sum_total_co2e.update_yaxes(range=[0, 100000000000], autorange=False)
    fig_sum_total_co2e.update_layout(
        title=dict(text="Total CO<sub>2e</sub> emitted by passenger cars per year in kg"), # , font=dict(size=15, color="lightgray", family="verdana")
        margin=dict(l=20, r=20, t=80, b=20),
        yaxis_title="CO<sub>2e</sub> in kg",
        barmode="stack",
        plot_bgcolor='#003442',
        paper_bgcolor='#003442',
        font_color='white',
    )
    emission_target_2030 = selected_scenario_df['emission_target_de_30'].iloc[0]
    fig_sum_total_co2e.add_trace(
        go.Bar(
            x=['CO<sub>2e</sub> target <br> Germany 2030'],
            y=[emission_target_2030],
            marker_color=clr.green1_base,
            name='target 2030',
            text=['{:}B'.format(emission_target_2030 / 1000000000)],
        )
    )
    emission_target_2040 = selected_scenario_df['emission_target_de_40'].iloc[0]
    fig_sum_total_co2e.add_trace(
        go.Bar(
            x=['CO<sub>2e</sub> target <br> Germany 2040'],
            y=[emission_target_2040],
            marker_color=clr.maygreen_base,
            name='target 2040',
            # text=int(emission_target_2040 * (10 ** (-9))),
            text=['{:}B'.format(emission_target_2040 / 1000000000)],
        )
     )
    fig_sum_total_co2e.update_traces(width=0.4, textposition='outside')
    # fig_sum_total_co2e.add_annotation(x=['Co<sub>2e</sub> of <br> chosen scenario'], y=[y_icev_sum], text="mio t", showarrow=True)
    return fig_sum_total_co2e


def get_fig_co2e_segment_all_vehicle_classes(co2e_dataframe, chosen_segment):
    """
        Create a Plotly figure representing CO2 emissions for all vehicle classes within a chosen segment.

        This function takes a Pandas DataFrame containing CO2 emissions data, a chosen vehicle segment, and a color map.
        It generates a Plotly bar chart visualizing the CO2 emissions for all vehicle classes within the selected segment.

        :param pd.DataFrame co2e_dataframe:
            A Pandas DataFrame containing CO2 emissions data.

        :param str chosen_segment:
            The selected vehicle segment for which CO2 emissions will be visualized.

        :param Dict[str, Any] map_colors:
            A dictionary representing the KIT color map for different vehicle classes.

        :return: go.Figure
            A Plotly figure representing CO2 emissions for all vehicle classes within the chosen segment.
        """
    x_val = co2e_dataframe.loc[(slice(None), f"{chosen_segment}"), "co2e"]
    fig_co2e_segment_all_vehicle_classes = px.bar(x_val.to_frame('co2e'),
                                                  x=x_val.to_frame('co2e').index.get_level_values(0),
                                                  y='co2e',
                                                  color_discrete_map=map_colors,
                                                  # text=['{:.2}'.format(n / 1000) for n in x_val],
                                                  text_auto='.2s',
                                                  color=x_val.to_frame('co2e').index.get_level_values(0)
                                                  )
    fig_co2e_segment_all_vehicle_classes.update_layout(
            title='CO<sub>2e</sub> created by usage per year in kg',
            yaxis_title="CO<sub>2e</sub> in kg",
            xaxis_title="vehicle class",
            plot_bgcolor='#003442',
            paper_bgcolor='#003442',
            font_color='white',
            barmode='relative',
            hovermode="x unified")
    # fig_co2e_segment_all_vehicle_classes.update_yaxes(range=[0, 8000000000], autorange=False)
    fig_co2e_segment_all_vehicle_classes.update_traces(width=0.6)
    return fig_co2e_segment_all_vehicle_classes


def get_fig_consumption_l(co2e_dataframe, chosen_segments, chosen_vehicle_class):
    """
       Create a Plotly figure representing fuel consumption for a chosen vehicle class and segments.

       This function takes a Pandas DataFrame containing fuel consumption data, a chosen vehicle class,
       selected segments, and a color map. It generates a Plotly horizontal bar chart visualizing fuel consumption
       for each segment within the selected vehicle class.

       :param pd.DataFrame co2e_dataframe:
           A Pandas DataFrame containing fuel consumption data.

       :param str chosen_vehicle_class:
           The selected vehicle class (by user) for which fuel consumption will be visualized.

       :param List[str] chosen_segments:
           The selected vehicle segments (by user) for which fuel consumption will be visualized.

       :param Dict[str, Any] map_colors:
           A dictionary representing the KIT color map for different vehicle segments.

       :return: go.Figure
           A Plotly figure representing fuel consumption for a chosen vehicle class and segments.
       """
    consumption_segments = co2e_dataframe.loc[(chosen_vehicle_class, chosen_segments), "consumption_manufacturer_l"].to_frame('consumption')
    fig_consumption = px.bar(data_frame=consumption_segments,
                             y=consumption_segments.index.get_level_values(0),
                             x='consumption',
                             orientation='h',
                             barmode='group',
                             color=consumption_segments.index.get_level_values(1),
                             color_discrete_map=map_colors,
                             text_auto='.2s',
                             hover_name=co2e_dataframe.loc[(chosen_vehicle_class, chosen_segments), "used_model"])
    fig_consumption.update_layout(
            title='Fuel consumption per car in liter per 100 km',
            yaxis_title="vehicle class",
            xaxis_title="l/100km",
            legend_title="segment",
            plot_bgcolor='#002b36',
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='group',
    )
    fig_consumption.update_xaxes(range=[0, 30], autorange=False)
    fig_consumption.update_traces(width=0.2)
    return fig_consumption


def get_fig_consumption_kwh(co2e_dataframe, chosen_segments, chosen_vehicle_class):
    """
           Create a Plotly figure representing electricity consumption for a chosen vehicle class and segments.

           This function takes a Pandas DataFrame containing electricity consumption data, a chosen vehicle class,
           selected segments, and a color map. It generates a Plotly horizontal bar chart visualizing electricity consumption
           for each segment within the selected vehicle class.

           :param pd.DataFrame co2e_dataframe:
               A Pandas DataFrame containing electricity consumption data.

           :param str chosen_vehicle_class:
               The selected vehicle class (by user) for which fuel consumption will be visualized.

           :param List[str] chosen_segments:
               The selected vehicle segments (by user) for which fuel consumption will be visualized.

           :param Dict[str, Any] map_colors:
               A dictionary representing the KIT color map for different vehicle segments.

           :return: go.Figure
               A Plotly figure representing electricity consumption for a chosen vehicle class and segments.
           """
    consumption_segments = co2e_dataframe.loc[(chosen_vehicle_class, chosen_segments), "consumption_manufacturer_kWh"].to_frame('consumption')
    fig_consumption_kwh = px.bar(data_frame=consumption_segments, y=consumption_segments.index.get_level_values(0), x='consumption', orientation='h', barmode='group', color=consumption_segments.index.get_level_values(1), color_discrete_map=map_colors, text_auto='.2s')
    fig_consumption_kwh.update_layout(
            title='Electricity consumption per car in kWh per 100 km',
            yaxis_title="vehicle class",
            legend_title="segment",
            plot_bgcolor='#002b36',
            paper_bgcolor='#002b36',
            font_color='white',
            barmode='group',
    )
    fig_consumption_kwh.update_xaxes(range=[0, 25], autorange=False)
    return fig_consumption_kwh


def get_fig_production_comparison_per_year(co2_per_car, segment):
    """
       Create a Plotly figure representing the accumulated CO2 emissions of different powertrains per year.

       This function takes two Pandas DataFrames containing CO2 emissions data for different powertrains and their
       corresponding production CO2 emissions for one car. It generates a Plotly scatter plot visualizing the accumulated
       CO2 emissions for ICEV, HEV, PHEV, and BEV over a range of years.

       :param pd.DataFrame co2_per_car:
           A Pandas DataFrame containing usage CO2 emissions data for different powertrains.

       :param pd.DataFrame co2e_production_one_car:
           A Pandas DataFrame containing production CO2 emissions for one car for different powertrains.

       :param str segment:
           The selected vehicle segment (by user) for which the production comparison will be visualized.

       :return: go.Figure
           A Plotly figure representing the accumulated CO2 emissions of different powertrains per year.
       """
    x = np.arange(20)
    fig_production_comparison_per_year = go.Figure(go.Scatter(
        x=x,
        y=co2_per_car.loc['ICEV', f"{segment}"] * x + co2e_production_one_car.loc['ICEV', f"{segment}"],
        name='ICEV'
    ))
    fig_production_comparison_per_year.add_trace(go.Scatter(
        x=x,
        y=co2_per_car.loc['HEV', f"{segment}"] * x + co2e_production_one_car.loc['HEV', f"{segment}"],
        name='HEV'
    ))
    fig_production_comparison_per_year.add_trace(go.Scatter(
        x=x,
        y=co2_per_car.loc['PHEV', f"{segment}"] * x + co2e_production_one_car.loc['PHEV', f"{segment}"],
        name='PHEV'
    ))
    fig_production_comparison_per_year.add_trace(go.Scatter(
        x=x,
        y=co2_per_car.loc['BEV', f"{segment}"] * x + co2e_production_one_car.loc['BEV', f"{segment}"],
        name='BEV'
    ))
    fig_production_comparison_per_year.update_layout(
        title='Accumulated CO<sub>2e</sub> of different powertrains per year',
        yaxis_title="CO<sub>2e</sub> in kg",
        xaxis_title="year",
        plot_bgcolor='#003442',
        paper_bgcolor='#003442',
        font_color='white',
    )
    return fig_production_comparison_per_year


def get_fig_production_comparison_per_km(co2_per_car_per_km, segment):
    """
       Create a Plotly figure representing the accumulated CO2 emissions of different powertrains per kilometer.

       This function takes two Pandas DataFrames containing usage CO2 emissions data for different powertrains and their
       corresponding production CO2 emissions for one car. It generates a Plotly scatter plot visualizing the accumulated
       CO2 emissions for ICEV, HEV, PHEV, and BEV over a range of years.

       :param pd.DataFrame co2_per_car:
           A Pandas DataFrame containing CO2 usage emissions data for different powertrains.

       :param pd.DataFrame co2e_production_one_car:
           A Pandas DataFrame containing production CO2 emissions for one car for different powertrains.

       :param str segment:
           The selected vehicle segment (by user) for which the production comparison will be visualized.

       :return: go.Figure
           A Plotly figure representing the accumulated CO2 emissions of different powertrains per kilometer.
       """
    x = np.arange(300000)

    fig_production_comparison_per_km = go.Figure(go.Scatter(
        x=x,
        y=co2_per_car_per_km.loc['ICEV', f"{segment}"] * x + co2e_production_one_car.loc['ICEV', f"{segment}"],
        name='ICEV'
    ))
    fig_production_comparison_per_km.add_trace(go.Scatter(
        x=x,
        y=co2_per_car_per_km.loc['HEV', f"{segment}"] * x + co2e_production_one_car.loc['HEV', f"{segment}"],
        name='HEV'
    ))
    fig_production_comparison_per_km.add_trace(go.Scatter(
        x=x,
        y=co2_per_car_per_km.loc['PHEV', f"{segment}"] * x + co2e_production_one_car.loc['PHEV', f"{segment}"],
        name='PHEV'
    ))
    fig_production_comparison_per_km.add_trace(go.Scatter(
        x=x,
        y=co2_per_car_per_km.loc['BEV', f"{segment}"] * x + co2e_production_one_car.loc['BEV', f"{segment}"],
        name='BEV'
    ))
    fig_production_comparison_per_km.update_layout(
        title='accumulated CO<sub>2e</sub> of different powertrains per km',
        yaxis_title="CO<sub>2e</sub> in kg",
        xaxis_title="km",
        plot_bgcolor='#003442',
        paper_bgcolor='#003442',
        font_color='white',
    )
    return fig_production_comparison_per_km


def get_fig_scenario_comparison(chosen_scenario_list, chosen_unit):
    """
        Create a Plotly figure representing a comparison between different scenarios.

        This function takes a unit of measurement, a list of chosen scenarios, and generates a Plotly horizontal bar chart
        visualizing the total CO2 emissions for each scenario based on the chosen unit of measurement.

        :param str chosen_unit:
            The chosen unit of measurement.

        :param Union[str, List[str]] chosen_scenario_list:
            Either a single scenario name or a list of scenario names to be compared (chosen by user).

        :return: go.Figure
            A Plotly figure representing the comparison between different scenarios.
        """
    chosen_unit = str(chosen_unit).lower()
    fig_comparison = go.Figure()
    if not type(chosen_scenario_list) == list:
        chosen_scenario_list = [chosen_scenario_list]
    for scenario_name in chosen_scenario_list:
        current_scenario_df = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{scenario_name}', sep=';', decimal=",", thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[5])
        scenario_var = calculate_variables_based_on_scenario(current_scenario_df)
        fig_comparison.add_trace(
            go.Bar(
                y=[str(scenario_name).replace('_', ' ').replace('.CSV', '').replace('.csv', '')],
                x=[scenario_var[f"co2e_{chosen_unit}_per_segment"].sum()],
                orientation='h',
                marker_color=clr.green1_base,
                text=int(scenario_var[f"co2e_{chosen_unit}_per_segment"].sum()*(10**(-9))),
            )
        )
        fig_comparison.update_layout(
            title='Comparison between different scenarios',
            yaxis_title="Scenarios",
            xaxis_title="CO<sub>2e</sub> in mio t",
            legend_title_text="LCA",
            plot_bgcolor='#003442',
            paper_bgcolor='#003442',
            font_color='white',
            barmode='group',
            autosize=True,
            showlegend=False,
        )
    fig_comparison.update_xaxes(range=[0, 100000000000], autorange=False)
    fig_comparison.update_traces(width=0.5)
    return fig_comparison


def get_fig_lca_waterfall(chosen_scenario_name, chosen_lca, chosen_vehicle_class, chosen_segment, is_recycling_displayed):
    """
        Create a Plotly figure representing a waterfall plot for the life cycle assessment (LCA) of a single car.

        This function takes parameters such as the scenario name, LCA type, vehicle class, segment, and a flag indicating
        whether recycling is displayed. It generates a Plotly waterfall chart visualizing the LCA of a single car with
        different components including production, usage, recycling, and total CO2 emissions.

        :param str chosen_scenario_name:
            The name of the chosen scenario.

        :param str chosen_lca:
            The chosen type of life cycle assessment (LCA).

        :param str chosen_vehicle_class:
            The selected vehicle class for which the LCA will be visualized.

        :param str chosen_segment:
            The selected vehicle segment for which the LCA will be visualized.

        :param bool is_recycling_displayed:
            A flag indicating whether recycling is displayed.

        :return: go.Figure
            A Plotly figure representing the waterfall plot for the life cycle assessment of a single car.
        """
    chosen_scenario_df = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{chosen_scenario_name}', sep=';', decimal=",",
                                     thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True,
                                     header=[5])
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
        y_value = [co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], (co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'])*10.1, co2e_per_single_car_savings.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_total]
        x_value = ["production", "usage", "recycling", "total co2e"]
        measure = ["relative", "relative", "relative", "total"]
    elif is_recycling_displayed is False:
        print("is_recycling_displayed is False")
        co2e_per_single_car_total = co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e']
        y_value = [co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], (co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'])*10.1, co2e_per_single_car_total]
        x_value = ["production", "usage", "total co2e"]
        measure = ["relative", "relative", "total"]
    else:
        co2e_per_single_car_total = co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'] + co2e_per_single_car_savings.loc[(chosen_vehicle_class, chosen_segment), 'co2e']
        y_value = [co2e_per_single_car_production.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], (co2e_per_single_car_usage.loc[(chosen_vehicle_class, chosen_segment), 'co2e'])*10.1, co2e_per_single_car_savings.loc[(chosen_vehicle_class, chosen_segment), 'co2e'], co2e_per_single_car_total]
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
        title="LCA of a single car with a lifetime expectancy of 10.1 years",
        showlegend=True,
        plot_bgcolor='#003442',
        paper_bgcolor='#003442',
        font_color='white'
    )
    return fig_lca_waterfall


def get_yearly_co2_fig():
    """
        Create a Plotly figure representing the annual and accumulated CO2 emissions of passenger cars in Germany from 1990
        until 2050.

        This function takes the data of a selected scenario containing data on CO2 emissions. It generates
        a Plotly bar chart representing the annual CO2 emissions per year and a cumulative line chart for the accumulated
        CO2 emissions since 2022. It also includes a dashed line representing the allowed CO2 budget left.

        :param pd.DataFrame selected_scenario:
            A Pandas DataFrame containing data on CO2 emissions, paths, and budgets.

        :return: go.Figure
            A Plotly figure representing the annual and accumulated CO2 emissions of passenger cars in Germany.
        """
    x_since_1990 = [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,
                    2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    y_since_1990 = [110000000000, 112200000000, 116280000000, 119000000000, 116280000000, 119000000000, 119000000000,
                    119000000000, 121000000000, 125000000000, 123000000000, 120000000000, 119000000000, 114920000000,
                    114240000000, 108000000000, 106000000000, 104000000000, 104000000000, 104000000000, 104000000000,
                    104000000000, 104000000000, 107440000000, 108000000000, 109000000000, 111000000000, 113000000000,
                    110000000000]
    x = numpy.array([2019, 2030, 2045])
    y = numpy.array([111520000000, selected_scenario['path_emission_2030'].iloc[0], selected_scenario['path_emission_2045'].iloc[0]])
    x_new = numpy.arange(2019, 2050, 1)
    x_array_combined = numpy.concatenate((x_since_1990, x_new))
    yearly_co2e_regression = [max(0, reg_val) for reg_val in calc.calc_quadratic_regression(x=x, y=y, x_new=x_new)]
    y_array_combined = numpy.concatenate((y_since_1990, yearly_co2e_regression))
    yearly_co2e_fig = go.Figure(data=go.Bar(
        x=x_array_combined,
        y=y_array_combined,
        marker_color=clr.green1_base,
        name="CO<sub>2e</sub> per year",
    ))
    yearly_co2e_fig.add_trace(go.Scatter(
        x=x_array_combined[-28:],
        y=numpy.cumsum(y_array_combined[-28:]),
        yaxis='y2',
        name="accumulated CO<sub>2e</sub>",
        line=dict(color="#007A63"),
        )
    )
    yearly_co2e_fig.add_shape(
        type="line",
        xref="paper",
        yref="y2",
        x0=0,
        y0=804712000000,
        x1=1,
        y1=804712000000,
        line=dict(color="darkgrey", dash="dash"),
        label=dict(text="allowed CO<sub>2e</sub> budget", font=dict(color="white"))
        )
    yearly_co2e_fig.update_layout(
        title='CO<sub>2e</sub> of passenger cars in Germany from 1990 until 2050',
        yaxis_title="co2e in kg",
        xaxis_title="year",
        plot_bgcolor='#003442',
        paper_bgcolor='#003442',
        font_color='white',
        barmode='relative',
        hovermode="x unified",
        yaxis=dict(
            title=dict(text="CO<sub>2e</sub> per year"),
            side="left",
            range=[0, 120000000000]
        ),
        yaxis2=dict(
            title=dict(text="CO<sub>2e</sub> accumulated since 2022"),
            side="right",
            range=[0, 2250000000000],
            overlaying="y",
            tickmode="sync",
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.85
        )
    )
    return yearly_co2e_fig


def get_parameter_menu_content(filename_of_scenario):
    """
       Initialize global variables based on the selected scenario.

       This function initializes and computes various global variables related to the selected scenario. It includes
       calculations for shares of different fuels, CO2 emissions, and vehicle stock.

       :param str filename_of_scenario:
           The name of the selected scenario.

       :param Optional[pd.DataFrame] scenario_df:
           An optional Pandas DataFrame containing scenario data.

       :return: Tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float,
                      float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]
           A tuple containing various calculated global variables based on the selected scenario.
       """
    init_global_variables(selected_scenario_name=filename_of_scenario, scenario_df=None)
    global selected_scenario
    vehicle_classes_list_without_lkw = list(dict.fromkeys(selected_scenario.index.get_level_values(0).to_list()))
    vehicle_classes_list_without_lkw.remove('lkw')

    share_e5 = selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'].unique()
    share_e10 = selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'].unique()
    share_diesel = selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'].unique()
    share_hvo = selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_hvo_totaldiesel'].unique()
    share_ptl = selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_ptl_totalgasoline'].unique()
    share_bioliq = selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_bioliq_totalgasoline'].unique()
    co2e_electricity = selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'].unique()

    df_icev = selected_scenario.loc[('ICEV', slice(None))]
    icev_g_vehicle_stock = df_icev.loc[df_icev['energysupply'] == 'gasoline', 'total_number_of_cars_in_vehicle_class'][0]
    icev_g_share = icev_g_vehicle_stock / selected_scenario['number_of_cars_in_segment'].sum()

    icev_d_vehicle_stock = df_icev.loc[df_icev['energysupply'] == 'diesel', 'total_number_of_cars_in_vehicle_class'][0]
    icev_d_share = icev_d_vehicle_stock / selected_scenario['number_of_cars_in_segment'].sum()

    df_hev = selected_scenario.loc[('HEV', slice(None))]
    hev_g_vehicle_stock = df_hev.loc[df_icev['energysupply'] == 'gasoline', 'total_number_of_cars_in_vehicle_class'][0]
    hev_g_share = hev_g_vehicle_stock / selected_scenario['number_of_cars_in_segment'].sum()

    hev_d_vehicle_stock = df_hev.loc[df_icev['energysupply'] == 'diesel', 'total_number_of_cars_in_vehicle_class'][0]
    hev_d_share = hev_d_vehicle_stock / selected_scenario['number_of_cars_in_segment'].sum()

    phev_vehicle_stock = selected_scenario.loc[('PHEV', slice(None)), 'total_number_of_cars_in_vehicle_class'][0]
    phev_share = phev_vehicle_stock / selected_scenario['number_of_cars_in_segment'].sum()

    bev_vehicle_stock = selected_scenario.loc[('BEV', slice(None)), 'total_number_of_cars_in_vehicle_class'][0]
    bev_share = bev_vehicle_stock / selected_scenario['number_of_cars_in_segment'].sum()

    co2e_e5_ttw = float(selected_scenario['co2e_E5_TtW'].unique())
    co2e_e10_ttw = float(selected_scenario['co2e_E10_TtW'].unique())
    co2e_b7_ttw = float(selected_scenario['co2e_D7_TtW'].unique())
    co2e_hvo_ttw = float(selected_scenario['co2e_ptl_TtW'].unique())
    co2e_ptl_ttw = float(selected_scenario['co2e_ptl_TtW'].unique())
    co2e_bioliq_ttw = float(selected_scenario['co2e_bioliq_TtW'].unique())
    co2e_e5_wtw = float(selected_scenario['co2e_E5_WtW'].unique())
    co2e_e10_wtw = float(selected_scenario['co2e_E10_WtW'].unique())
    co2e_b7_wtw = float(selected_scenario['co2e_D7_WtW'].unique())
    co2e_hvo_wtw = float(selected_scenario['co2e_hvo_WtW'].unique())
    co2e_ptl_wtw = float(selected_scenario['co2e_ptl_WtW'].unique())
    co2e_bioliq_wtw = float(selected_scenario['co2e_bioliq_WtW'].unique())

    vehicle_stock = float(selected_scenario['number_of_cars_in_segment'].sum() * 10 ** (-6))
    share_hev_g = float(hev_g_share * 100)
    share_hev_d = float(hev_d_share * 100)
    share_icev_g = float(icev_g_share * 100)
    share_icev_d = float(icev_d_share * 100)
    share_phev = float(phev_share * 100)
    share_bev = float(bev_share * 100)
    share_diesel = float(share_diesel * 100)
    share_hvo = float(share_hvo * 100)
    share_ptl = float(share_ptl * 100)
    share_bioliq = float(share_bioliq * 100)
    share_e5 = float(share_e5 * 100)
    share_e10 = float(share_e10 * 100)
    co2e_electricity = float(co2e_electricity * 1000)

    return share_e5, share_e10, share_diesel, share_hvo, share_ptl, share_bioliq, co2e_electricity, vehicle_stock, share_icev_g, share_icev_d, share_hev_g, share_hev_d, share_phev, share_bev, co2e_e5_ttw, co2e_e10_ttw, co2e_b7_ttw, co2e_hvo_ttw, co2e_ptl_ttw, co2e_bioliq_ttw, co2e_e5_wtw, co2e_e10_wtw, co2e_b7_wtw, co2e_hvo_wtw, co2e_ptl_wtw, co2e_bioliq_wtw

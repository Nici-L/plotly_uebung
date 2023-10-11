'''import plotly.graph_objects as go
import plotly.express as px
import source.utils.colors_KIT_plotly as clr
import pandas as pd
import source.utils.calculations as calc
import source.config as config
import numpy

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


# the following functions are for creating the graphs
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
        print("nix!")
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
        title="LCA of a single car",
        showlegend=True,
        plot_bgcolor='#002b36',  # color Solar stylesheet
        paper_bgcolor='#002b36',
        font_color='white'
    )
    return fig_lca_waterfall


def get_yearly_co2_fig(regression_array, x_array):
    yearly_co2e_fig = go.Figure(data=go.Bar(x=x_array, y=regression_array, marker_color=clr.green1_base))
    yearly_co2e_fig.add_trace(
        go.Scatter(
            x=x_array[-30:],
            y=numpy.cumsum(regression_array[-30:]),
            yaxis='y2',
        )
    )
    yearly_co2e_fig.add_shape(type="line", xref="paper", yref="y2", x0=0, y0=1220000000000, x1=1, y1=1220000000000, line=dict(
        color="red",
        dash="dash"
    ),
                              )
    yearly_co2e_fig.update_layout(
        title='Co<sub>2e</sub> of passenger cars in Germany from 1990 until 2050',
        yaxis_title="co2e in kg",
        xaxis_title="",
        plot_bgcolor='#002b36',  # color Solar stylesheet
        paper_bgcolor='#002b36',
        font_color='white',
        barmode='relative',
        hovermode="x unified",
        yaxis=dict(
            title=dict(text="Total number of diners"),
            side="left",
        ),
        yaxis2=dict(
            title=dict(text="Total bill amount"),
            side="right",
            range=[0, 2250000000000],
            overlaying="y",
            tickmode="sync",
        ),
        showlegend=False,
    )
    return yearly_co2e_fig'''
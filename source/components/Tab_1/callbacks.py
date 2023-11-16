from dash import html, dcc, Output, Input, State, no_update
import source.components.Tab_1.figures as fig
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import source.config as config


# callback for scenario dropdown
def register_callbacks(app_instance):
    @app_instance.callback(
        Output(component_id='output_input_div', component_property='children', allow_duplicate=True),
        Input(component_id='scenario-dropdown', component_property='value'),
        prevent_initial_call=True
    )
    def update_scenario_selection(scenario_chosen):

        fig.init_global_variables(selected_scenario_name=scenario_chosen)
        return f'You have selected: {scenario_chosen}'

    # callback for parameter menu when calculate button is pressed
    @app_instance.callback(
        Output(component_id='output_input_div', component_property='children', allow_duplicate=True),
        Input(component_id='calculate-button', component_property='n_clicks'),
        [
         State(component_id='share_E5', component_property='value'),
         State(component_id='share_E10', component_property='value'),
         State(component_id='share_diesel', component_property='value'),
         State(component_id='co2e_electricity', component_property='value'),
         State(component_id='vehicle_stock', component_property='value'),
         State(component_id='share_icev_g', component_property='value'),
         State(component_id='share_icev_d', component_property='value'),
         State(component_id='share_hev', component_property='value'),
         State(component_id='share_phev', component_property='value'),
         State(component_id='share_bev', component_property='value'),
        ],
        prevent_initial_call=True
    )
    def update_parameter_menu_calculate_button(n, share_E5, share_E10, share_diesel, co2e_electricity, vehicle_stock, share_icev_g, share_icev_d, share_hev, share_phev, share_bev):
        share_hev = share_hev/100
        share_icev_g = share_icev_g/100
        share_icev_d = share_icev_d/100
        share_phev = share_phev/100
        share_bev = share_bev/100
        share_diesel = share_diesel/100
        share_E5 = share_E5/100
        share_E10 = share_E10/100
        vehicle_stock = vehicle_stock*1000000
        co2e_electricity = co2e_electricity/1000
        vehicle_classes_list_without_lkw = list(dict.fromkeys(fig.selected_scenario.index.get_level_values(0).to_list()))
        vehicle_classes_list_without_lkw.remove('lkw')

        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'] = share_E5
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'] = share_E10
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'] = share_diesel
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'] = co2e_electricity
        fig.selected_scenario['vehicle_stock'] = fig.selected_scenario['shareontotalvehicles'] * vehicle_stock

        df_icev = fig.selected_scenario.loc[('icev', slice(None))]
        vehicle_stock_icev_g = vehicle_stock * share_icev_g
        df_icev.loc[df_icev['energysupply'] == 'gasoline', 'vehicle_stock'] = vehicle_stock_icev_g * df_icev.loc[df_icev['energysupply'] == 'gasoline', 'share_on_total_vehicles_of_class']

        vehicle_stock_icev_d = vehicle_stock * share_icev_d
        df_icev.loc[df_icev['energysupply'] == 'diesel', 'vehicle_stock'] = vehicle_stock_icev_d * df_icev.loc[df_icev['energysupply'] == 'diesel', 'share_on_total_vehicles_of_class']

        df_hev = fig.selected_scenario.loc[('hev', slice(None))]
        vehicle_stock_hev = vehicle_stock * share_hev
        df_hev.loc[df_icev['energysupply'] == 'gasoline', 'vehicle_stock'] = vehicle_stock_hev * df_hev.loc[df_icev['energysupply'] == 'gasoline', 'share_on_total_vehicles_of_class']

        vehicle_stock_phev = vehicle_stock * share_phev
        fig.selected_scenario.loc[('phev', slice(None)), 'vehicle_stock'] = vehicle_stock_phev * fig.selected_scenario.loc[('phev', slice(None)), 'share_on_total_vehicles_of_class']

        vehicle_stock_bev = vehicle_stock * share_bev
        fig.selected_scenario.loc[('bev', slice(None)), 'vehicle_stock'] = vehicle_stock_bev * fig.selected_scenario.loc[('bev', slice(None)), 'share_on_total_vehicles_of_class']

        fig.init_global_variables(selected_scenario_name=None, scenario_df=fig.selected_scenario)

        return f'you have selected your own custom scenario'


# update parameter menu when new scenario is chosen
    @app_instance.callback(
        # State(component_id='input_consumption', component_property='value'),
        [
            Output(component_id='share_E5', component_property='value'),
            Output(component_id='share_E10', component_property='value'),
            Output(component_id='share_diesel', component_property='value'),
            Output(component_id='share_HVO', component_property='value'),
            Output(component_id='share_PtL', component_property='value'),
            Output(component_id='share_bioliq', component_property='value'),
            Output(component_id='co2e_electricity', component_property='value'),
            Output(component_id='vehicle_stock', component_property='value'),
            Output(component_id='share_icev_g', component_property='value'),
            Output(component_id='share_icev_d', component_property='value'),
            Output(component_id='share_hev', component_property='value'),
            Output(component_id='share_phev', component_property='value'),
            Output(component_id='share_bev', component_property='value'),
            Output(component_id='co2e_E5', component_property='value'),
            Output(component_id='co2e_E10', component_property='value'),
            Output(component_id='co2e_diesel', component_property='value'),
            Output(component_id='co2e_HVO', component_property='value'),
            Output(component_id='co2e_PtL', component_property='value'),
            Output(component_id='co2e_bioliq', component_property='value'),
        ],
        Input(component_id='output_input_div', component_property='children'),
    )
    def update_parameter_menu(scenario_selection_string):

        fig.init_global_variables(selected_scenario_name=None, scenario_df=fig.selected_scenario)
        vehicle_classes_list_without_lkw = list(dict.fromkeys(fig.selected_scenario.index.get_level_values(0).to_list()))
        vehicle_classes_list_without_lkw.remove('lkw')

        share_E5 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'].unique()
        share_E10 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'].unique()
        share_diesel = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'].unique()
        share_hvo = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_hvo_totaldiesel'].unique()
        share_ptl = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_ptl_totalgasoline'].unique()
        share_bioliq = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_bioliq_totalgasoline'].unique()
        co2e_electricity = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'].unique()

        df_icev = fig.selected_scenario.loc[('icev', slice(None))]
        icev_g_vehicle_stock = df_icev.loc[df_icev['energysupply'] == 'gasoline', 'total_number_of_cars_in_class'][0]
        icev_g_share = icev_g_vehicle_stock/fig.selected_scenario['vehicle_stock'].sum()

        icev_d_vehicle_stock = df_icev.loc[df_icev['energysupply'] == 'diesel', 'total_number_of_cars_in_class'][0]
        icev_d_share = icev_d_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        df_hev = fig.selected_scenario.loc[('hev', slice(None))]
        hev_g_vehicle_stock = df_hev.loc[df_icev['energysupply'] == 'gasoline', 'total_number_of_cars_in_class'][0]
        hev_g_share = hev_g_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        phev_vehicle_stock = fig.selected_scenario.loc[('phev', slice(None)), 'total_number_of_cars_in_class'][0]
        phev_share = phev_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        bev_vehicle_stock = fig.selected_scenario.loc[('bev', slice(None)), 'total_number_of_cars_in_class'][0]
        bev_share = bev_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        co2e_e5_ttw = float(fig.selected_scenario['co2e_E5_TtW'].unique())
        co2e_e10_ttw = float(fig.selected_scenario['co2e_E10_TtW'].unique())
        co2e_b7_ttw = float(fig.selected_scenario['co2e_D7_TtW'].unique())
        co2e_hvo_ttw = float(fig.selected_scenario['co2e_hvo_TtW'].unique())
        co2e_ptl_ttw = float(fig.selected_scenario['co2e_ptl_TtW'].unique())
        co2e_bioliq_ttw = float(fig.selected_scenario['co2e_bioliq_TtW'].unique())

        vehicle_stock = int(fig.selected_scenario['vehicle_stock'].sum())
        share_hev = int(hev_g_share * 100)
        share_icev_g = int(icev_g_share * 100)
        share_icev_d = int(icev_d_share * 100)
        share_phev = int(phev_share * 100)
        share_bev = int(bev_share * 100)
        share_diesel = int(share_diesel * 100)
        share_hvo = int(share_hvo*100)
        share_ptl = int(share_ptl*100)
        share_bioliq = int(share_bioliq*100)
        share_E5 = int(share_E5 * 100)
        share_E10 = int(share_E10 * 100)
        co2e_electricity = int(co2e_electricity * 1000)

        # share_hev = ((1 / fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('hev', slice(None)), 'vehicle_stock']).sum()
        # fig.selected_scenario.loc[('icev', slice(None)), 'vehicle_stock'] = vehicle_stock_icev_g * fig.selected_scenario.loc[('icev', slice(None)), 'share_on_total_vehicles_of_class']
        # selected_scenario.loc[('hev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_hev) * selected_scenario.loc[('hev', slice(None)), 'shareontotalvehicles']

        return share_E5, share_E10, share_diesel, share_hvo, share_ptl, share_bioliq, co2e_electricity, vehicle_stock, share_icev_g, share_icev_d, share_hev, share_phev, share_bev, co2e_e5_ttw, co2e_e10_ttw, co2e_b7_ttw, co2e_hvo_ttw, co2e_ptl_ttw, co2e_bioliq_ttw


# callback for reset button
    @app_instance.callback(
        # State(component_id='input_consumption', component_property='value'),
        [Output(component_id='share_E5', component_property='value', allow_duplicate=True),
         Output(component_id='share_E10', component_property='value', allow_duplicate=True),
         Output(component_id='share_diesel', component_property='value', allow_duplicate=True),
         Output(component_id='share_HVO', component_property='value', allow_duplicate=True),
         Output(component_id='share_PtL', component_property='value', allow_duplicate=True),
         Output(component_id='share_bioliq', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_electricity', component_property='value', allow_duplicate=True),
         Output(component_id='vehicle_stock', component_property='value', allow_duplicate=True),
         Output(component_id='share_icev_g', component_property='value', allow_duplicate=True),
         Output(component_id='share_icev_d', component_property='value', allow_duplicate=True),
         Output(component_id='share_hev', component_property='value', allow_duplicate=True),
         Output(component_id='share_phev', component_property='value', allow_duplicate=True),
         Output(component_id='share_bev', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_E5', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_E10', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_diesel', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_HVO', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_PtL', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_bioliq', component_property='value', allow_duplicate=True),
         ],
        Input(component_id='reset-button', component_property='n_clicks'),
        State(component_id='scenario-dropdown', component_property='value'),
        prevent_initial_call=True
    )
    def update_parameter_menu_reset_button(scenario_selection_string, scenario_chosen):

        fig.init_global_variables(selected_scenario_name=None, scenario_df=fig.selected_scenario)
        vehicle_classes_list_without_lkw = list(dict.fromkeys(fig.selected_scenario.index.get_level_values(0).to_list()))
        vehicle_classes_list_without_lkw.remove('lkw')

        share_E5 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'].unique()
        share_E10 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'].unique()
        share_diesel = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'].unique()
        share_hvo = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_hvo_totaldiesel'].unique()
        share_ptl = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_ptl_totalgasoline'].unique()
        share_bioliq = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_bioliq_totalgasoline'].unique()
        co2e_electricity = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'].unique()

        df_icev = fig.selected_scenario.loc[('icev', slice(None))]
        icev_g_vehicle_stock = df_icev.loc[df_icev['energysupply'] == 'gasoline', 'total_number_of_cars_in_class'][0]
        icev_g_share = icev_g_vehicle_stock/fig.selected_scenario['vehicle_stock'].sum()

        icev_d_vehicle_stock = df_icev.loc[df_icev['energysupply'] == 'diesel', 'total_number_of_cars_in_class'][0]
        icev_d_share = icev_d_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        df_hev = fig.selected_scenario.loc[('hev', slice(None))]
        hev_g_vehicle_stock = df_hev.loc[df_icev['energysupply'] == 'gasoline', 'total_number_of_cars_in_class'][0]
        hev_g_share = hev_g_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        phev_vehicle_stock = fig.selected_scenario.loc[('phev', slice(None)), 'total_number_of_cars_in_class'][0]
        # phev_g_vehicle_stock = df_phev.loc[df_icev['energysupply'] == 'gasoline'
        phev_share = phev_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        bev_vehicle_stock = fig.selected_scenario.loc[('bev', slice(None)), 'total_number_of_cars_in_class'][0]
        bev_share = bev_vehicle_stock / fig.selected_scenario['vehicle_stock'].sum()

        co2e_e5_ttw = float(fig.selected_scenario['co2e_E5_TtW'].unique())
        co2e_e10_ttw = float(fig.selected_scenario['co2e_E10_TtW'].unique())
        co2e_b7_ttw = float(fig.selected_scenario['co2e_D7_TtW'].unique())
        co2e_hvo_ttw = float(fig.selected_scenario['co2e_hvo_TtW'].unique())
        co2e_ptl_ttw = float(fig.selected_scenario['co2e_ptl_TtW'].unique())
        co2e_bioliq_ttw = float(fig.selected_scenario['co2e_bioliq_TtW'].unique())

        vehicle_stock = int(fig.selected_scenario['vehicle_stock'].sum())
        share_hev = int(hev_g_share * 100)
        share_icev_g = int(icev_g_share * 100)
        share_icev_d = int(icev_d_share * 100)
        share_phev = int(phev_share * 100)
        share_bev = int(bev_share * 100)
        share_diesel = int(share_diesel * 100)
        share_hvo = int(share_hvo * 100)
        share_ptl = int(share_ptl * 100)
        share_bioliq = int(share_bioliq * 100)
        share_E5 = int(share_E5 * 100)
        share_E10 = int(share_E10 * 100)
        co2e_electricity = int(co2e_electricity * 1000)

        return share_E5, share_E10, share_diesel,share_hvo, share_ptl, share_bioliq, co2e_electricity, vehicle_stock, share_icev_g, share_icev_d, share_hev, share_phev, share_bev, co2e_e5_ttw, co2e_e10_ttw, co2e_b7_ttw, co2e_hvo_ttw, co2e_ptl_ttw, co2e_bioliq_ttw

    # callback for TtW or WtW button
    @app_instance.callback(
        Output("co2e_ttw_barchart", "figure"),
        [Input("display_figure", "value"),
         Input(component_id='output_input_div', component_property='children')],
        prevent_initital_call=True
    )
    def update_total_co2e_graph(display_figure, input):
        if display_figure == 'TtW':
            fig_sum_total_co2e = fig.get_fig_sum_total_co2e(fig.co2e_ttw_per_segment, fig.selected_scenario)
            return fig_sum_total_co2e
        elif display_figure == 'WtW':
            fig_sum_total_co2e = fig.get_fig_sum_total_co2e(fig.co2e_wtw_per_segment, fig.selected_scenario)
        else:
            fig_sum_total_co2e = {}
        return fig_sum_total_co2e

    # callback for segment and TtW dropdown
    @app_instance.callback(
        Output('co2e_ttw_barchart_car', 'figure'),
        [Input('TtW_vehicle_class_fig', 'value'),
         Input('choose-segments', 'value'),
         Input('one_car_dropdown', 'value'),
         Input(component_id='output_input_div', component_property='children')],
    )
    def update_car_graph(chosen_lc_step, chosen_segment, car_number, input):
        if chosen_lc_step == 'TtW' and car_number == 'all vehicles':
            fig_co2e_segment_all_vehicle_classes = fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_ttw_per_segment_df, chosen_segment)
            return fig_co2e_segment_all_vehicle_classes
        elif chosen_lc_step == 'WtW' and car_number == 'all vehicles':
            fig_co2e_segment_all_vehicle_classes = fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_wtw_per_segment_df, chosen_segment)
            return fig_co2e_segment_all_vehicle_classes
        elif chosen_lc_step == 'TtW' and car_number == 'one car':
            fig_co2e_segment_all_vehicle_classes = fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_ttw_per_car_df, chosen_segment)
            return fig_co2e_segment_all_vehicle_classes
        elif chosen_lc_step == 'WtW' and car_number == 'one car':
            fig_co2e_segment_all_vehicle_classes = fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_wtw_per_car_df, chosen_segment)
            return fig_co2e_segment_all_vehicle_classes
        else:
            fig_co2e_segment_all_vehicle_classes = {}
        return fig_co2e_segment_all_vehicle_classes

    # callback for segment and vehicle class dropdown
    @app_instance.callback(
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
            fig_consumption = fig.get_fig_consumption(fig.selected_scenario, chosen_segments, slice(None))
            return fig_consumption
        elif chosen_unit == 'liter' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) == 1:
            fig_consumption = fig.get_fig_consumption(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            return fig_consumption
        elif chosen_unit == 'liter' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) >= 1:
            fig_consumption = fig.get_fig_consumption(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            return fig_consumption

        elif chosen_unit == 'kWh' and chosen_vehicle_class is None or len(chosen_vehicle_class) == 0 and chosen_segments is None or len(chosen_segments) == 0 or None:
            return no_update
        elif chosen_unit == 'kWh' and len(chosen_vehicle_class) == 0 and len(chosen_segments) == 1:
            fig_consumption = fig.get_fig_consumption_kwh(fig.selected_scenario, chosen_segments, slice(None))
            return fig_consumption
        elif chosen_unit == 'kWh' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) == 1:
            fig_consumption = fig.get_fig_consumption_kwh(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            return fig_consumption
        elif chosen_unit == 'kWh' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) >= 1:
            fig_consumption = fig.get_fig_consumption_kwh(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            return fig_consumption
        else:
            return no_update

    # callback for scenario comparison
    @app_instance.callback(
        Output('scenario-comparison', 'figure'),
        [Input('scenario-dropdown-comparison', 'value'),
         Input('chose_lca_comparison_fig', 'value'),
         Input(component_id='details-toggle-option', component_property='value')],
        prevent_initital_call=True
    )
    def update_comparison_graph(chosen_scenario_list, chosen_unit, show_details):
        fig_comparison = fig.get_fig_scenario_comparison(chosen_scenario_list=chosen_scenario_list, chosen_unit=chosen_unit)
        return fig_comparison

    @app_instance.callback(
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
        fig_lca_waterfall = fig.get_fig_lca_waterfall(chosen_scenario_name=chosen_scenario, chosen_lca=chosen_lca, chosen_vehicle_class=chosen_vehicle_class, chosen_segment=chosen_segment, is_recycling_displayed=is_recycling_displayed)
        return fig_lca_waterfall

    @app_instance.callback(
        Output(component_id='fig_production_comparison', component_property='figure'),
        Input(component_id='output_input_div', component_property='children'),
        Input(component_id='chose_lca_scatter_plot', component_property='value'),
        Input(component_id='lca-segment-production-comparison', component_property='value'),
        Input(component_id='chose_km_or_year', component_property='value'),
        prevent_initital_call=True
    )
    def update_production_comparison_graph(input_div, chosen_lca, chosen_segment, km_or_year_value):
        if chosen_lca == 'TtW' and km_or_year_value == 'per year':
            fig_production_comparison = fig.get_fig_production_comparison_per_year(co2_per_car=fig.co2e_ttw_per_car, segment=chosen_segment)
            return fig_production_comparison
        elif chosen_lca == 'WtW' and km_or_year_value == 'per year':
            fig_production_comparison = fig.get_fig_production_comparison_per_year(co2_per_car=fig.co2e_wtw_per_car, segment=chosen_segment)
            return fig_production_comparison
        elif chosen_lca == 'TtW' and km_or_year_value == 'per km':
            fig_production_comparison = fig.get_fig_production_comparison_per_km(co2_per_car_per_km=fig.co2e_ttw_per_car_per_km, segment=chosen_segment)
            return fig_production_comparison
        elif chosen_lca == 'WtW' and km_or_year_value == 'per km':
            fig_production_comparison = fig.get_fig_production_comparison_per_km(co2_per_car_per_km=fig.co2e_wtw_per_car_per_km, segment=chosen_segment)
            return fig_production_comparison
        else:
            fig_production_comparison = {}
        return fig_production_comparison

    @app_instance.callback(
        Output("co2e_over_the_years_fig", "figure"),
        Input(component_id='output_input_div', component_property='children'),
        prevent_initital_call=True
    )
    def update_total_co2e_graph(input):
        yearly_co2_fig = fig.get_yearly_co2_fig()
        return yearly_co2_fig

    @app_instance.callback(
        Output("collapse", "is_open"),
        [Input("collapse-button-1", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app_instance.callback(
        Output("collapse 2", "is_open"),
        [Input("collapse-button-2", "n_clicks")],
        [State("collapse 2", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app_instance.callback(
        Output("collapse 3", "is_open"),
        [Input("collapse-button-3", "n_clicks")],
        [State("collapse 3", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app_instance.callback(
        Output("collapse 4", "is_open"),
        [Input("collapse-button-4", "n_clicks")],
        [State("collapse 4", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app_instance.callback(
        Output("collapse 5", "is_open"),
        [Input("collapse-button-5", "n_clicks")],
        [State("collapse 5", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app_instance.callback(
        Output("modal-xl", "is_open"),
        Input("open-xl", "n_clicks"),
        State("modal-xl", "is_open"),
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open
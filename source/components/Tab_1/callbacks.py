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
        return f'You have selected: {scenario_chosen} at {datetime.now().strftime("%d.%m.%y %H:%M:%S")}'


    # callback for parameter menu when calculate button is pressed
    @app_instance.callback(
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
    def update_parameter_menu_calculate_button(n, share_E5, share_E10, share_diesel, co2e_electricity, vehicle_stock, share_icev_g, share_hev, share_phev, share_bev):
        share_hev = share_hev/100
        share_icev_g = share_icev_g/100
        share_phev = share_phev/100
        share_bev = share_bev/100
        share_diesel = share_diesel/100
        share_E5 = share_E5/100
        share_E10 = share_E10/100
        vehicle_stock = vehicle_stock*1000000
        co2e_electricity = co2e_electricity/1000
        vehicle_classes_list_without_lkw = list(dict.fromkeys(fig.selected_scenario.index.get_level_values(0).to_list()))
        vehicle_classes_list_without_lkw.remove('lkw')
        # selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'consumption_manufacturer_l'] = consumption
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'] = share_E5
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'] = share_E10
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'] = share_diesel
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'] = co2e_electricity
        fig.selected_scenario['vehicle_stock'] = fig.selected_scenario['shareontotalvehicles'] * vehicle_stock
        vehicle_stock_icev_g = vehicle_stock * share_icev_g
        # print(f"icev_g share:{share_icev_g}")
        # print(f"vehicle stock icev_g:{vehicle_stock_icev_g}")
        fig.selected_scenario.loc[('icev', slice(None)), 'vehicle_stock'] = vehicle_stock_icev_g * fig.selected_scenario.loc[('icev', slice(None)), 'share_on_total_vehicles_of_class']

        # fig.selected_scenario.loc[('icev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_icev) * fig.selected_scenario.loc[('icev', slice(None)), 'shareontotalvehicles']
        fig.selected_scenario.loc[('hev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_hev) * fig.selected_scenario.loc[('hev', slice(None)), 'shareontotalvehicles']
        fig.selected_scenario.loc[('phev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_phev) * fig.selected_scenario.loc[('phev', slice(None)), 'shareontotalvehicles']
        fig.selected_scenario.loc[('bev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_bev) * fig.selected_scenario.loc[('bev', slice(None)), 'shareontotalvehicles']

        fig.init_global_variables(selected_scenario_name=None, scenario_df=fig.selected_scenario)

        return f'you have selected your own custom scenario at {datetime.now().strftime("%d.%m.%y %H:%M:%S")}'


# update parameter menu when new scenario is chosen
    @app_instance.callback(
        # State(component_id='input_consumption', component_property='value'),
        [Output(component_id='share_E5', component_property='value', allow_duplicate=True),
        Output(component_id='share_E10', component_property='value', allow_duplicate=True),
        Output(component_id='share_diesel', component_property='value', allow_duplicate=True),
        Output(component_id='co2e_electricity', component_property='value', allow_duplicate=True),
        Output(component_id='vehicle_stock', component_property='value', allow_duplicate=True),
        Output(component_id='share_icev', component_property='value', allow_duplicate=True),
        Output(component_id='share_hev', component_property='value', allow_duplicate=True),
        Output(component_id='share_phev', component_property='value', allow_duplicate=True),
        Output(component_id='share_bev', component_property='value', allow_duplicate=True), ],
        Input(component_id='output_input_div', component_property='children'),

        prevent_initial_call=True
    )
    def update_parameter_menu(scenario_selection_string):

        fig.init_global_variables(selected_scenario_name=None, scenario_df=fig.selected_scenario)

        vehicle_classes_list_without_lkw = list(dict.fromkeys(fig.selected_scenario.index.get_level_values(0).to_list()))
        vehicle_classes_list_without_lkw.remove('lkw')

        share_E5 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'].unique()
        share_E10 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'].unique()
        share_diesel = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'].unique()
        co2e_electricity = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'].unique()

        # share_icev = (fig.selected_scenario.loc[('icev', slice(None)), 'total_number_of_cars_in_class'] & fig.selected_scenario.loc['energysupply'] == 'gasoline')/fig.selected_scenario['vehicle_stock'].sum()
        # print(f"number of icev_g{fig.selected_scenario.loc[('icev', slice(None)), 'total_number_of_cars_in_class'] & fig.selected_scenario.loc['energysupply'] == 'gasoline'}")

        # icev_vehicle_stock = fig.selected_scenario.loc[('icev', slice(None))].loc[(fig.selected_scenario['energysupply'] == 'gasoline'), 'total_number_of_cars_in_class']
        icev_vehicle_stock = fig.selected_scenario.loc[('icev', slice(None)) & ('energysupply' == 'gasoline')][ 'total_number_of_cars_in_class']
        # (fig.selected_scenario['energysupply'] == 'gasoline'), 'total_number_of_cars_in_class'
        #icev_g = fig.selected_scenario['energysupply'] == 'gasoline'
        print(f"icev_g vehicle stock {icev_vehicle_stock}")
        # df.loc[(df['Salary_in_1000'] >= 100) & (df['Age'] < 60) & (df['FT_Team'].str.startswith('S')), ['Name', 'FT_Team']]

        share_hev = ((1 / fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('hev', slice(None)), 'vehicle_stock']).sum()
        share_bev = ((1 / fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('bev', slice(None)), 'vehicle_stock']).sum()
        share_phev = ((1 / fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('phev', slice(None)), 'vehicle_stock']).sum()
        vehicle_stock = int(fig.selected_scenario['vehicle_stock'].sum())
        share_hev = int(share_hev * 100)
        share_icev = 100
        share_phev = int(share_phev * 100)
        share_bev = int(share_bev * 100)
        share_diesel = int(share_diesel * 100)
        share_E5 = int(share_E5 * 100)
        share_E10 = int(share_E10 * 100)
        co2e_electricity = int(co2e_electricity * 1000)

        fig.selected_scenario['vehicle_stock'] = fig.selected_scenario['shareontotalvehicles'] * vehicle_stock
        print(f"vehicle stock per segment: {fig.selected_scenario['vehicle_stock']}")
        # vehicle_stock_icev_g = vehicle_stock * share_icev_g
        # print(f"icev_g share:{share_icev_g}")
        # print(f"vehicle stock icev_g:{vehicle_stock_icev_g}")
        # fig.selected_scenario.loc[('icev', slice(None)), 'vehicle_stock'] = vehicle_stock_icev_g * fig.selected_scenario.loc[('icev', slice(None)), 'share_on_total_vehicles_of_class']
        # selected_scenario.loc[('hev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_hev) * selected_scenario.loc[('hev', slice(None)), 'shareontotalvehicles']
        # selected_scenario.loc[('phev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_phev) * selected_scenario.loc[('phev', slice(None)), 'shareontotalvehicles']
        # selected_scenario.loc[('bev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_bev) * selected_scenario.loc[('bev', slice(None)), 'shareontotalvehicles']

        return share_E5, share_E10, share_diesel, co2e_electricity, vehicle_stock, share_icev, share_hev, share_phev, share_bev


# callback for reset button
    @app_instance.callback(
        # State(component_id='input_consumption', component_property='value'),
        [Output(component_id='share_E5', component_property='value'),
        Output(component_id='share_E10', component_property='value'),
        Output(component_id='share_diesel', component_property='value'),
        Output(component_id='co2e_electricity', component_property='value'),
        Output(component_id='vehicle_stock', component_property='value'),
        Output(component_id='share_icev', component_property='value'),
        Output(component_id='share_hev', component_property='value'),
        Output(component_id='share_phev', component_property='value'),
        Output(component_id='share_bev', component_property='value'),],
        Input(component_id='reset-button', component_property='n_clicks'),
        State(component_id='scenario-dropdown', component_property='value'),
        prevent_initial_call=True
    )
    def update_parameter_menu_reset_button(scenario_selection_string, scenario_chosen):
        fig.init_global_variables(selected_scenario_name=scenario_chosen)

        vehicle_classes_list_without_lkw = list(dict.fromkeys(fig.selected_scenario.index.get_level_values(0).to_list()))
        vehicle_classes_list_without_lkw.remove('lkw')

        share_E5 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'].unique()
        share_E10 = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'].unique()
        share_diesel = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'].unique()
        co2e_electricity = fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'].unique()
        share_icev = ((1/fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('icev', slice(None)), 'vehicle_stock']).sum()
        share_hev = ((1 / fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('hev', slice(None)), 'vehicle_stock']).sum()
        share_bev = ((1 / fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('bev', slice(None)), 'vehicle_stock']).sum()
        share_phev = ((1 / fig.selected_scenario['vehicle_stock'].sum()) * fig.selected_scenario.loc[('phev', slice(None)), 'vehicle_stock']).sum()

        # selected_scenario.loc[('hev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_hev) * selected_scenario.loc[('hev', slice(None)), 'shareontotalvehicles']
        # selected_scenario.loc[('phev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_phev) * selected_scenario.loc[('phev', slice(None)), 'shareontotalvehicles']
        # selected_scenario.loc[('bev', slice(None)), 'vehicle_stock'] = (vehicle_stock * share_bev) * selected_scenario.loc[('bev', slice(None)), 'shareontotalvehicles']


        share_hev = int(share_hev*100)
        share_icev = int(share_icev*100)
        share_phev = int(share_phev*100)
        share_bev = int(share_bev*100)
        share_diesel = int(share_diesel*100)
        share_E5 = int(share_E5*100)
        share_E10 = int(share_E10*100)
        vehicle_stock = int(fig.selected_scenario['vehicle_stock'].sum())
        co2e_electricity = int(co2e_electricity * 1000)

        return share_E5, share_E10, share_diesel, co2e_electricity, vehicle_stock, share_icev, share_hev, share_phev, share_bev

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
        chosen_unit = str(chosen_unit).lower()
        if not type(chosen_scenario_list) == list:
            chosen_scenario_list = [chosen_scenario_list]
        fig_comparison = go.Figure()
        for scenario_name in chosen_scenario_list:
            current_scenario_df = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{scenario_name}', sep=';', decimal=",", thousands='.', encoding="ISO-8859-1", index_col=[0, 1], skipinitialspace=True, header=[3])
            scenario_var = fig.calculate_variables_based_on_scenario(current_scenario_df)
            fig_comparison.add_trace(
                go.Bar(
                    y=[str(scenario_name).replace('_', ' ').replace('.CSV', '').replace('.csv', '')],
                    x=[scenario_var[f"co2e_{chosen_unit}_per_segment"].sum()],
                    orientation='h',
                    marker_color=fig.clr.green1_base,
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
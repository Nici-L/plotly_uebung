from dash import html, dcc, Output, Input, State, no_update
import source.components.Tab_1.figures as fig
import plotly.graph_objects as go
import os
import pandas as pd
import source.config as config
import source.utils.calculations as calc


scenario_filenames = []
for file in os.listdir(config.SCENARIO_FOLDER_PATH):
    scenario_data = pd.read_csv(f'{config.SCENARIO_FOLDER_PATH}/{file}', sep=';', encoding="ISO-8859-1")
    year = scenario_data.iloc[0][0]
    model_name = scenario_data.iloc[0][1]
    if file.endswith('.CSV') or file.endswith('.csv'):
        # scenario_filenames.append(file)
        scenario_filenames.append({
            'value': file,
            'label': file.replace('_', ' ').replace('.CSV', '').replace('.csv', ''),
            'year': year,
            'modelname': model_name,
        })

# todo:rename radioitems input
# callback for scenario dropdown
def register_callbacks(app_instance):
    @app_instance.callback(
        Output(component_id='output_input_div', component_property='children', allow_duplicate=True),
        Input(component_id='radioitems-input', component_property='value'),
        Input(component_id='scenario-dropdown', component_property='value'),
        prevent_initial_call=True
    )
    def update_scenario_selection(selected_scenario_year, selected_scenario_modelname):
        print(f"selected year:{selected_scenario_year}")
        print(f"selected name:{selected_scenario_modelname}")
        scenario_chosen = calc.get_unique_values_from_dict(data=scenario_filenames, key_of_interest='value', condition_dict={'modelname': selected_scenario_modelname, 'year': selected_scenario_year})[0]
        fig.init_global_variables(selected_scenario_name=scenario_chosen)
        return f'You have selected: {scenario_chosen}'

    @app_instance.callback(
        Output(component_id='radioitems-input', component_property='options'),
        Output(component_id='radioitems-input', component_property='value'),
        Input(component_id='scenario-dropdown', component_property='value'),
        prevent_initial_call=True
    )
    def update_year_buttons(selected_scenario_modelname):
        years = calc.get_unique_values_from_dict(data=scenario_filenames, key_of_interest='year', condition_dict={'modelname': selected_scenario_modelname})
        default_year = years[0]
        return years, default_year

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
         State(component_id='share_hev_g', component_property='value'),
         State(component_id='share_hev_d', component_property='value'),
         State(component_id='share_phev', component_property='value'),
         State(component_id='share_bev', component_property='value'),
         State(component_id='co2e_E5_ttw', component_property='value'),
         State(component_id='co2e_E10_ttw', component_property='value'),
         State(component_id='co2e_diesel_ttw', component_property='value'),
         State(component_id='co2e_HVO_ttw', component_property='value'),
         State(component_id='co2e_PtL_ttw', component_property='value'),
         State(component_id='co2e_bioliq_ttw', component_property='value'),
         State(component_id='co2e_E5_wtw', component_property='value'),
         State(component_id='co2e_E10_wtw', component_property='value'),
         State(component_id='co2e_diesel_wtw', component_property='value'),
         State(component_id='co2e_HVO_wtw', component_property='value'),
         State(component_id='co2e_PtL_wtw', component_property='value'),
         State(component_id='co2e_bioliq_wtw', component_property='value'),
        ],
        prevent_initial_call=True
    )
    def update_parameter_menu_calculate_button(n, share_e5, share_e10, share_diesel, co2e_electricity, vehicle_stock, share_icev_g, share_icev_d, share_hev_g, share_hev_d, share_phev, share_bev, co2e_e5_ttw, co2e_e10_ttw, co2e_b7_ttw, co2e_hvo_ttw, co2e_ptl_ttw,co2e_bioliq_ttw, co2e_e5_wtw, co2e_e10_wtw, co2e_b7_wtw, co2e_hvo_wtw, co2e_ptl_wtw, co2e_bioliq_wtw):
        share_hev_g = share_hev_g/100
        share_hev_d = share_hev_d/100
        share_icev_g = share_icev_g/100
        share_icev_d = share_icev_d/100
        share_phev = share_phev/100
        share_bev = share_bev/100
        share_diesel = share_diesel/100
        share_e5 = share_e5/100
        share_e10 = share_e10/100
        vehicle_stock = vehicle_stock*1000000
        co2e_electricity_kg = co2e_electricity/1000
        fig.selected_scenario['co2e_E5_TtW'] = co2e_e5_ttw
        fig.selected_scenario['co2e_E10_TtW'] = co2e_e10_ttw
        fig.selected_scenario['co2e_D7_TtW'] = co2e_b7_ttw
        fig.selected_scenario['co2e_hvo_TtW'] = co2e_hvo_ttw
        fig.selected_scenario['co2e_ptl_TtW'] = co2e_ptl_ttw
        fig.selected_scenario['co2e_bioliq_TtW'] = co2e_bioliq_ttw

        fig.selected_scenario['co2e_E5_WtW'] = co2e_e5_wtw
        fig.selected_scenario['co2e_E10_WtW'] = co2e_e10_wtw
        fig.selected_scenario['co2e_D7_WtW'] = co2e_b7_wtw
        fig.selected_scenario['co2e_hvo_WtW'] = co2e_hvo_wtw
        fig.selected_scenario['co2e_ptl_WtW'] = co2e_ptl_wtw
        fig.selected_scenario['co2e_bioliq_WtW'] = co2e_bioliq_wtw

        vehicle_classes_list_without_lkw = list(dict.fromkeys(fig.selected_scenario.index.get_level_values(0).to_list()))
        vehicle_classes_list_without_lkw.remove('lkw')

        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E5_totalgasoline'] = share_e5
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_E10_totalgasoline'] = share_e10
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'share_D7_totaldiesel'] = share_diesel
        fig.selected_scenario.loc[(vehicle_classes_list_without_lkw, slice(None)), 'co2e_electricity_WtW'] = co2e_electricity_kg
        # fig.selected_scenario['vehicle_stock'] = fig.selected_scenario['shareontotalvehicles'] * vehicle_stock

        df_icev = fig.selected_scenario.loc[('ICEV', slice(None)), :].copy()
        vehicle_stock_icev_g = vehicle_stock * share_icev_g
        # fig.selected_scenario.loc[('icev', slice(None))] = df_icev
        condition_icev_g = df_icev['energysupply'] == 'gasoline'
        df_icev.loc[condition_icev_g, 'number_of_cars_in_segment'] = vehicle_stock_icev_g * df_icev.loc[condition_icev_g, 'share_of_segment_on_total_vehicles_of_class']

        vehicle_stock_icev_d = vehicle_stock * share_icev_d
        condition_icev_d = df_icev['energysupply'] == 'diesel'
        df_icev.loc[condition_icev_d, 'number_of_cars_in_segment'] = vehicle_stock_icev_d * df_icev.loc[condition_icev_d, 'share_of_segment_on_total_vehicles_of_class']

        fig.selected_scenario.loc[('ICEV', slice(None))] = df_icev

        df_hev = fig.selected_scenario.loc[('HEV', slice(None)), :].copy()
        vehicle_stock_hev_g = vehicle_stock * share_hev_g
        condition_hev_g = df_hev['energysupply'] == 'gasoline'
        df_hev.loc[condition_hev_g, 'number_of_cars_in_segment'] = vehicle_stock_hev_g * df_hev.loc[condition_hev_g, 'share_of_segment_on_total_vehicles_of_class']

        vehicle_stock_hev_d = vehicle_stock * share_hev_d
        condition_hev_d = df_hev['energysupply'] == 'diesel'
        df_hev.loc[condition_hev_d, 'number_of_cars_in_segment'] = vehicle_stock_hev_d * df_hev.loc[condition_hev_d, 'share_of_segment_on_total_vehicles_of_class']
        # fig.selected_scenario.loc[('hev', slice(None))] = df_hev

        vehicle_stock_phev = vehicle_stock * share_phev
        fig.selected_scenario.loc[('PHEV', slice(None)), 'number_of_cars_in_segment'] = vehicle_stock_phev * fig.selected_scenario.loc[('phev', slice(None)), 'share_of_segment_on_total_vehicles_of_class']

        vehicle_stock_bev = vehicle_stock * share_bev
        fig.selected_scenario.loc[('BEV', slice(None)), 'number_of_cars_in_segment'] = vehicle_stock_bev * fig.selected_scenario.loc[('bev', slice(None)), 'share_of_segment_on_total_vehicles_of_class']

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
            Output(component_id='share_hev_g', component_property='value'),
            Output(component_id='share_hev_d', component_property='value'),
            Output(component_id='share_phev', component_property='value'),
            Output(component_id='share_bev', component_property='value'),
            Output(component_id='co2e_E5_ttw', component_property='value'),
            Output(component_id='co2e_E10_ttw', component_property='value'),
            Output(component_id='co2e_diesel_ttw', component_property='value'),
            Output(component_id='co2e_HVO_ttw', component_property='value'),
            Output(component_id='co2e_PtL_ttw', component_property='value'),
            Output(component_id='co2e_bioliq_ttw', component_property='value'),
            Output(component_id='co2e_E5_wtw', component_property='value'),
            Output(component_id='co2e_E10_wtw', component_property='value'),
            Output(component_id='co2e_diesel_wtw', component_property='value'),
            Output(component_id='co2e_HVO_wtw', component_property='value'),
            Output(component_id='co2e_PtL_wtw', component_property='value'),
            Output(component_id='co2e_bioliq_wtw', component_property='value'),
        ],
        Input(component_id='radioitems-input', component_property='value'),
        State(component_id='scenario-dropdown', component_property='value'),
    )
    def update_parameter_menu(year_of_selected_scenario, name_of_selected_scenario):
        _filename_of_selected_scenario = calc.get_unique_values_from_dict(
            data=scenario_filenames,
            key_of_interest='value',
            condition_dict={'modelname': name_of_selected_scenario, 'year': year_of_selected_scenario})[0]
        _parameter_inputs = fig.get_parameter_menu_content(filename_of_scenario=_filename_of_selected_scenario)
        return _parameter_inputs




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
         Output(component_id='share_hev_g', component_property='value', allow_duplicate=True),
         Output(component_id='share_hev_d', component_property='value', allow_duplicate=True),
         Output(component_id='share_phev', component_property='value', allow_duplicate=True),
         Output(component_id='share_bev', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_E5_ttw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_E10_ttw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_diesel_ttw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_HVO_ttw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_PtL_ttw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_bioliq_ttw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_E5_wtw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_E10_wtw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_diesel_wtw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_HVO_wtw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_PtL_wtw', component_property='value', allow_duplicate=True),
         Output(component_id='co2e_bioliq_wtw', component_property='value', allow_duplicate=True),
         ],
        Input(component_id='reset-button', component_property='n_clicks'),
        State(component_id='scenario-dropdown', component_property='value'),
        State(component_id='radioitems-input', component_property='value'),
        prevent_initial_call=True
    )
    def update_parameter_menu_reset_button(scenario_selection_string, name_of_selected_scenario, year_of_selected_scenario):
        _filename_of_selected_scenario = calc.get_unique_values_from_dict(
            data=scenario_filenames,
            key_of_interest='value',
            condition_dict={'modelname': name_of_selected_scenario, 'year': year_of_selected_scenario})[0]
        _parameter_inputs = fig.get_parameter_menu_content(filename_of_scenario=_filename_of_selected_scenario)
        return _parameter_inputs


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
        elif display_figure == 'WtW':
            fig_sum_total_co2e = fig.get_fig_sum_total_co2e(fig.co2e_wtw_per_segment, fig.selected_scenario)
        else:
            fig_sum_total_co2e = {}
        fig_sum_total_co2e.write_image("images/fig_sum_total_co2e.pdf")
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
            fig_co2e_segment_all_vehicle_classes.write_image("images/fig_co2e_segment_all_vehicle_classes.pdf")
            return fig_co2e_segment_all_vehicle_classes
        elif chosen_lc_step == 'WtW' and car_number == 'all vehicles':
            fig_co2e_segment_all_vehicle_classes = fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_wtw_per_segment_df, chosen_segment)
            fig_co2e_segment_all_vehicle_classes.write_image("images/fig_co2e_segment_all_vehicle_classes.pdf")
            return fig_co2e_segment_all_vehicle_classes
        elif chosen_lc_step == 'TtW' and car_number == 'one car':
            fig_co2e_segment_all_vehicle_classes = fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_ttw_per_car_df, chosen_segment)
            fig_co2e_segment_all_vehicle_classes.write_image("images/fig_co2e_segment_all_vehicle_classes.pdf")
            return fig_co2e_segment_all_vehicle_classes
        elif chosen_lc_step == 'WtW' and car_number == 'one car':
            fig_co2e_segment_all_vehicle_classes = fig.get_fig_co2e_segment_all_vehicle_classes(fig.co2e_wtw_per_car_df, chosen_segment)
            fig_co2e_segment_all_vehicle_classes.write_image("images/fig_co2e_segment_all_vehicle_classes.pdf")
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
            fig_consumption = fig.get_fig_consumption_l(fig.selected_scenario, chosen_segments, slice(None))
            fig_consumption.write_image("images/fig_consumption.pdf")
            return fig_consumption
        elif chosen_unit == 'liter' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) == 1:
            fig_consumption = fig.get_fig_consumption_l(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            fig_consumption.write_image("images/fig_consumption.pdf")
            return fig_consumption
        elif chosen_unit == 'liter' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) >= 1:
            fig_consumption = fig.get_fig_consumption_l(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            fig_consumption.write_image("images/fig_consumption.pdf")
            return fig_consumption

        elif chosen_unit == 'kWh' and chosen_vehicle_class is None or len(chosen_vehicle_class) == 0 and chosen_segments is None or len(chosen_segments) == 0 or None:
            return no_update
        elif chosen_unit == 'kWh' and len(chosen_vehicle_class) == 0 and len(chosen_segments) == 1:
            fig_consumption = fig.get_fig_consumption_kwh(fig.selected_scenario, chosen_segments, slice(None))
            fig_consumption.write_image("images/fig_consumption.pdf")
            return fig_consumption
        elif chosen_unit == 'kWh' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) == 1:
            fig_consumption = fig.get_fig_consumption_kwh(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            fig_consumption.write_image("images/fig_consumption.pdf")
            return fig_consumption
        elif chosen_unit == 'kWh' and len(chosen_vehicle_class) >= 1 and len(chosen_segments) >= 1:
            fig_consumption = fig.get_fig_consumption_kwh(fig.selected_scenario, chosen_segments, chosen_vehicle_class)
            fig_consumption.write_image("images/fig_consumption.pdf")
            return fig_consumption
        else:
            return no_update

    # callback for scenario comparison
    @app_instance.callback(
        Output('scenario-comparison', 'figure'),
        Input(component_id='details-toggle-option', component_property='value'),
        Input(component_id='selection-button-scenario-comparison', component_property='n_clicks'),
        [State('scenario-dropdown-comparison', 'value'),
         State('chose_lca_comparison_fig', 'value'),
         ],
        prevent_initital_call=True
    )
    def update_comparison_graph(show_details, n, chosen_scenario_list, chosen_unit):
        if chosen_scenario_list is None:
            fig_comparison = go.Figure()
            fig_comparison.update_layout(
                plot_bgcolor='#002b36',  # color Solar stylesheet
                paper_bgcolor='#002b36',
            )
        else:
            fig_comparison = fig.get_fig_scenario_comparison(chosen_scenario_list=chosen_scenario_list, chosen_unit=chosen_unit)
        fig_comparison.write_image("images/fig_comparison.pdf")
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
        fig_lca_waterfall.write_image("images/fig_lca_waterfall.pdf")
        return fig_lca_waterfall

    @app_instance.callback(
        Output(component_id='fig_production_comparison', component_property='figure'),
        Input(component_id='selection-button-vehicle-class-comparison', component_property='n_clicks'),
        Input(component_id='output_input_div', component_property='children'),
        State(component_id='chose_lca_scatter_plot', component_property='value'),
        State(component_id='lca-segment-production-comparison', component_property='value'),
        State(component_id='chose_km_or_year', component_property='value'),
        prevent_initital_call=True
    )
    def update_production_comparison_graph(n, input_div, chosen_lca, chosen_segment, km_or_year_value):
        if chosen_lca == 'TtW' and km_or_year_value == 'per year':
            fig_production_comparison = fig.get_fig_production_comparison_per_year(co2_per_car=fig.co2e_ttw_per_car, segment=chosen_segment)
            fig_production_comparison.write_image("images/fig_production_comparison.pdf")
            return fig_production_comparison
        elif chosen_lca == 'WtW' and km_or_year_value == 'per year':
            fig_production_comparison = fig.get_fig_production_comparison_per_year(co2_per_car=fig.co2e_wtw_per_car, segment=chosen_segment)
            fig_production_comparison.write_image("images/fig_production_comparison.pdf")
            return fig_production_comparison
        elif chosen_lca == 'TtW' and km_or_year_value == 'per km':
            fig_production_comparison = fig.get_fig_production_comparison_per_km(co2_per_car_per_km=fig.co2e_ttw_per_car_per_km, segment=chosen_segment)
            fig_production_comparison.write_image("images/fig_production_comparison.pdf")
            return fig_production_comparison
        elif chosen_lca == 'WtW' and km_or_year_value == 'per km':
            fig_production_comparison = fig.get_fig_production_comparison_per_km(co2_per_car_per_km=fig.co2e_wtw_per_car_per_km, segment=chosen_segment)
            fig_production_comparison.write_image("images/fig_production_comparison.pdf")
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
        yearly_co2_fig.write_image("images/yearly_co2_fig.pdf")
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
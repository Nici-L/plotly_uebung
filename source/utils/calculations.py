import pandas as pd


def get_vehicle_class(df_data: pd.DataFrame):
    vehicle_class_list = df_data.index.get_level_values(0).unique()
    print(f"vehicle_class_list: {vehicle_class_list}")
    return vehicle_class_list


# function for getting segments
def get_segments_per_vehicle_class(df_data: pd.DataFrame):
    for vehicle_class in get_vehicle_class(df_data):
        segments_per_vehicle_class = df_data.loc[vehicle_class]
        print(f"all vehicle classes and their segments: {segments_per_vehicle_class}")
    return segments_per_vehicle_class # only last for loop is being saved and will remain the index for following calculations


def get_consumption_manufacturer_liter(df_data: pd.DataFrame):
    consumption_manufacturer_liter = df_data['consumption_manufacturer_l']
    return consumption_manufacturer_liter


def get_consumption_manufacturer_kwh(df_data: pd.DataFrame):
    consumption_manufacturer_kwh = df_data['consumption_manufacturer_kWh']
    return consumption_manufacturer_kwh


def get_consumption_per_year(consumption_per_100km, df_data):
    consumption_per_km = consumption_per_100km/100
    consumption_per_year = consumption_per_km*df_data['mileage']
    return consumption_per_year


'''def add_column_from_dataframe(series, df_dataframe, column_name):
    added_column = series.to_frame().join(column_name)
    return added_column'''


def get_co2e_usage_ttw(series_with_energy_supply, df_data):
    for ind in series_with_energy_supply.index:
        row = series_with_energy_supply.loc[[ind]]
        print(f"current row: {row}")
        '''
        if row['energysupply'] == 'gasoline':
            calculate_co2e_gasoline = series_with_energy_supply * (df_data['share_E5_totalgasoline'] * df_data['co2e_E5_TtW'] + df_data['share_E10_totalgasoline'] * df_data['co2e_E10_TtW'])
        '''



    '''  
        if series_with_energy_supply['energysupply'] == 'gasoline':
        calculate_co2e_gasoline = series_with_energy_supply * (df_data['share_E5_totalgasoline'] * df_data['co2e_E5_TtW'] + df_data['share_E10_totalgasoline'] * df_data['co2e_E10_TtW'])
        return calculate_co2e_gasoline
         if series_with_energy_supply['energysupply'] == 'diesel':
        calculate_co2e_diesel = series_with_energy_supply
    '''






def get_co2e_fuel(df_data):
    co2e_E5_TtW = df_data['co2e_E5_TtW']
    return co2e_E5_TtW


'''def combine_consumptions(consumption1, consumption2, df_data):
    combined_consumptions = consumption1.combine_first(consumption2)
    combined_consumptions_order = combined_consumptions.reindex_like(df_data)
    return combined_consumptions_order'''





import pandas as pd
import numpy
from matplotlib import pyplot as plt


def calculate_yearly_consumption_liter(df_data: pd.DataFrame):
    """
        Calculate yearly fuel consumption in liters based on manufacturer's data.

        :param df_data: (pd.DataFrame) A DataFrame containing vehicle data, including manufacturer's consumption and mileage.

        :return: (pandas Series) A Series containing the calculated yearly fuel consumption in liters for each vehicle.

        Example:
            df = pd.DataFrame({'Vehicle': ['Car1', 'Car2', 'Car3'],
                               'consumption_manufacturer_l': [6.5, 8.0, 7.2],
                               'mileage': [15000, 20000, 18000]})
            yearly_consumption = calculate_yearly_consumption_liter(df)
        """
    consumption_manufacturer_liter_per_km = df_data['consumption_manufacturer_l']/100
    consumption_manufacturer_liter_per_year = consumption_manufacturer_liter_per_km * df_data['mileage']
    # print(f"{consumption_manufacturer_liter_per_year}")
    return consumption_manufacturer_liter_per_year


def calculate_yearly_consumption_kwh(df_data: pd.DataFrame):
    """
        Calculate yearly energy consumption in kilowatt-hours (kWh) based on manufacturer's data.

        :param df_data: (pd.DataFrame) A DataFrame containing vehicle data, including manufacturer's energy consumption
                        in kilowatt-hours (kWh) and mileage.

        :return: (pandas Series) A Series containing the calculated yearly energy consumption in kilowatt-hours (kWh)
                 for each vehicle.

        Example:
            df = pd.DataFrame({'Vehicle': ['Car1', 'Car2', 'Car3'],
                               'consumption_manufacturer_kWh': [15, 20, 18],
                               'mileage': [15000, 20000, 18000]})
            yearly_consumption = calculate_yearly_consumption_kwh(df)
        """
    consumption_manufacturer_kwh_per_km = df_data['consumption_manufacturer_kWh']/100
    consumption_manufacturer_kwh_per_year = consumption_manufacturer_kwh_per_km * df_data['mileage']
    return consumption_manufacturer_kwh_per_year


def calculate_consumption_liter_per_km(df_data: pd.DataFrame):
    """
        Calculate yearly fuel consumption in liters based on manufacturer's data.

        :param df_data: (pd.DataFrame) A DataFrame containing vehicle data, including manufacturer's consumption and mileage.

        :return: (pandas Series) A Series containing the calculated yearly fuel consumption in liters for each vehicle.

        Example:
            df = pd.DataFrame({'Vehicle': ['Car1', 'Car2', 'Car3'],
                               'consumption_manufacturer_l': [6.5, 8.0, 7.2],
                               'mileage': [15000, 20000, 18000]})
            yearly_consumption = calculate_yearly_consumption_liter(df)
        """
    consumption_manufacturer_liter_per_km = df_data['consumption_manufacturer_l']/100
    return consumption_manufacturer_liter_per_km


def calculate_consumption_kwh_per_km(df_data: pd.DataFrame):
    """
        Calculate yearly energy consumption in kilowatt-hours (kWh) based on manufacturer's data.

        :param df_data: (pd.DataFrame) A DataFrame containing vehicle data, including manufacturer's energy consumption
                        in kilowatt-hours (kWh) and mileage.

        :return: (pandas Series) A Series containing the calculated yearly energy consumption in kilowatt-hours (kWh)
                 for each vehicle.

        Example:
            df = pd.DataFrame({'Vehicle': ['Car1', 'Car2', 'Car3'],
                               'consumption_manufacturer_kWh': [15, 20, 18],
                               'mileage': [15000, 20000, 18000]})
            yearly_consumption = calculate_yearly_consumption_kwh(df)
        """
    consumption_manufacturer_kwh_per_km = df_data['consumption_manufacturer_kWh']/100
    return consumption_manufacturer_kwh_per_km


def get_vehicle_class(df_data: pd.DataFrame):
    vehicle_class_list = df_data.index.get_level_values(0).unique()
    # print(f"vehicle_class_list: {vehicle_class_list}")
    return vehicle_class_list


def get_segments_per_vehicle_class(df_data: pd.DataFrame):
    """
     Calculate segments per vehicle class.

     :param df_data: (pd.DataFrame) A DataFrame containing vehicle class data.

     :return: (pd.DataFrame or None) A DataFrame with segments for each vehicle class if data is found,
              otherwise None.

     """
    segments_per_vehicle_class = None
    for vehicle_class in get_vehicle_class(df_data):
        segments_per_vehicle_class = df_data.loc[vehicle_class]
        # print(f"all vehicle classes and their segments: {segments_per_vehicle_class}")
    return segments_per_vehicle_class
    # only last for loop is being saved and will remain the index for following calculations


def get_consumption_per_year(consumption_per_100km, df_data):
    """
      Calculate annual fuel consumption for a given DataFrame of vehicles.

      :param consumption_per_100km: (float) Fuel consumption in liters per 100 kilometers.
      :param df_data: (pandas DataFrame) DataFrame containing vehicle mileage data.

      :return: (pandas Series) Series containing the calculated annual fuel consumption for each vehicle in df_data.

      Example:
          consumption_100km = 7.5  # liters per 100 kilometers
          mileage_data = pd.DataFrame({'Vehicle': ['Car1', 'Car2', 'Car3'],
                                       'mileage': [15000, 20000, 18000]})
          annual_consumption = get_consumption_per_year(consumption_100km, mileage_data)
      """
    consumption_per_km = consumption_per_100km/100
    consumption_per_year = consumption_per_km*df_data['mileage']
    return consumption_per_year


def get_co2e_usage_ttw_per_car_per_km(dataframe_consumption_per_km_liter_with_energy_supply, dataframe_consumption_per_km_kWh_with_energy_supply,  dataframe_with_co2e_values):
    """
        Calculate and return a pandas Series containing calculated CO2 equivalent emissions (CO2e) per car for each row in the input dataframe.

        This function calculates the CO2e emissions produced during the Tank-to-Wheel (TtT) phase of the vehicle energy supply chain
        based on the provided consumption data and operational characteristics.

        Parameters:
        :param dataframe_consumption_per_km_liter_with_energy_supply: (pandas DataFrame) A DataFrame containing consumption data in liters for each car.
        :param dataframe_consumption_per_km_kWh_with_energy_supply: (pandas DataFrame) A DataFrame containing consumption data in kilowatt-hours (kWh) for each car.
        :param dataframe_with_co2e_values: (pandas DataFrame) A DataFrame containing operational characteristics and energy supply information for each car.

        Returns:
        :return calculated_co2_series: (pandas Series) A Series containing the calculated CO2e emissions per car for each corresponding row in the input dataframe_with_co2e_values.

        Note:
        - The 'energysupply' column in dataframe_og is expected to have values 'gasoline', 'diesel', 'battery' or 'hybrid'.
        - CO2e emissions are calculated based on the energy supply type, consumption data, and CO2e factors provided in dataframe_og.
        - For 'gasoline' and 'diesel' energy supplies, CO2e emissions are calculated using consumption data in liters and appropriate CO2e factors.
        - For 'battery' energy supply, CO2e emissions are set to 0.
        - If the 'energysupply' column contains any other value, the calculated CO2e is set to NaN.
        """
    calculated_co2_series = pd.Series(index=dataframe_with_co2e_values.index)
    for ind in dataframe_with_co2e_values.index:
        row = dataframe_with_co2e_values.loc[ind]
        if row['energysupply'] == 'gasoline':
            calculated_co2e = dataframe_consumption_per_km_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_TtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_TtW']+ row['share_bioliq_totalgasoline'] * row['co2e_bioliq_TtW']+ row['share_ptl_totalgasoline'] * row['co2e_ptl_TtW'])
        elif row['energysupply'] == 'diesel':
            calculated_co2e = dataframe_consumption_per_km_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_D7_totaldiesel'] * row['co2e_D7_TtW'] + row['share_hvo_totaldiesel'] * row['co2e_hvo_TtW'])
        elif row['energysupply'] == 'battery':
            calculated_co2e = dataframe_consumption_per_km_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_TtW']
        elif row['energysupply'] == 'hybrid':
            calculated_co2e = dataframe_consumption_per_km_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_TtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_TtW']) + dataframe_consumption_per_km_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_TtW']
        else:
            calculated_co2e = None
        calculated_co2_series[ind] = calculated_co2e
    return calculated_co2_series


def get_co2e_usage_ttw_per_car(dataframe_consumption_per_year_liter_with_energy_supply, dataframe_consumption_per_year_kWh_with_energy_supply,  dataframe_with_co2e_values):
    """
        Calculate and return a pandas Series containing calculated CO2 equivalent emissions (CO2e) per car for each row in the input dataframe.

        This function calculates the CO2e emissions produced during the Well-to-Tank (WtT) phase of the vehicle energy supply chain
        based on the provided consumption data and operational characteristics.

        Parameters:
        :param dataframe_consumption_per_year_liter_with_energy_supply: (pandas DataFrame) A DataFrame containing consumption data in liters for each car.
        :param dataframe_consumption_per_year_kWh_with_energy_supply: (pandas DataFrame) A DataFrame containing consumption data in kilowatt-hours (kWh) for each car.
        :param dataframe_with_co2e_values: (pandas DataFrame) A DataFrame containing operational characteristics and energy supply information for each car.

        Returns:
        :return calculated_co2_series: (pandas Series) A Series containing the calculated CO2e emissions per car for each corresponding row in the input dataframe_with_co2e_values.

        Note:
        - The 'energysupply' column in dataframe_og is expected to have values 'gasoline', 'diesel', 'battery' or 'hybrid'.
        - CO2e emissions are calculated based on the energy supply type, consumption data, and CO2e factors provided in dataframe_og.
        - For 'gasoline' and 'diesel' energy supplies, CO2e emissions are calculated using consumption data in liters and appropriate CO2e factors.
        - For 'battery' energy supply, CO2e emissions are currently set to 0.
        - If the 'energysupply' column contains any other value, the calculated CO2e is set to NaN.
        """
    calculated_co2_series = pd.Series(index=dataframe_with_co2e_values.index)
    for ind in dataframe_with_co2e_values.index:
        row = dataframe_with_co2e_values.loc[ind]
        if row['energysupply'] == 'gasoline':
            calculated_co2e = dataframe_consumption_per_year_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_TtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_TtW']+ row['share_bioliq_totalgasoline'] * row['co2e_bioliq_TtW']+ row['share_ptl_totalgasoline'] * row['co2e_ptl_TtW'])
        elif row['energysupply'] == 'diesel':
            calculated_co2e = dataframe_consumption_per_year_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_D7_totaldiesel'] * row['co2e_D7_TtW'] + row['share_hvo_totaldiesel'] * row['co2e_hvo_TtW'])
        elif row['energysupply'] == 'battery':
            calculated_co2e = dataframe_consumption_per_year_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_TtW']
        elif row['energysupply'] == 'hybrid':
            calculated_co2e = dataframe_consumption_per_year_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_TtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_TtW']) + dataframe_consumption_per_year_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_TtW']
        else:
            calculated_co2e = None
        calculated_co2_series[ind] = calculated_co2e
    return calculated_co2_series


def get_co2e_usage_ttw_per_segment(series_with_calculated_co2e, dataframe_with_vehicle_stock):
    """
        Calculate the CO2 equivalent (CO2e) usage per segment based on a series of calculated CO2e values
        and a DataFrame containing vehicle stock information.

        :param series_with_calculated_co2e: A pandas Series with calculated CO2e values, where the index corresponds to segments.

        :type series_with_calculated_co2e: pd.Series

        :param dataframe_with_vehicle_stock: A pandas DataFrame containing information about vehicle stock,
                                             where each row represents a segment and includes at least a 'vehicle_stock' column.
        :type dataframe_with_vehicle_stock: pd.DataFrame

        :return: A pandas Series with calculated CO2e usage per segment, where the index corresponds to the segments
                 in the input DataFrame.
        :rtype: pd.Series

        This function iterates through the segments in the input DataFrame, multiplies the corresponding CO2e value
        from the series_with_calculated_co2e by the 'vehicle_stock' for each segment, and stores the result in
        calculated_co2e_per_segment_series.

        Note: The input Series and DataFrame must have matching indices for this function to work correctly.
        """
    calculated_co2e_per_segment_series = pd.Series(index=dataframe_with_vehicle_stock.index)
    for ind in dataframe_with_vehicle_stock.index:
        row = dataframe_with_vehicle_stock.loc[ind]
        calculated_co2e_per_segment = series_with_calculated_co2e[ind] * row['number_of_cars_in_segment']
        calculated_co2e_per_segment_series[ind] = calculated_co2e_per_segment
    return calculated_co2e_per_segment_series


def get_co2e_usage_wtw_per_car_per_km(dataframe_consumption_per_km_liter_with_energy_supply, dataframe_consumption_per_km_kWh_with_energy_supply,  dataframe_with_co2e_values):
    """
        Calculate the CO2 equivalent (CO2e) usage per car based on consumption data and CO2e values.

        :param dataframe_consumption_per_km_liter_with_energy_supply: A pandas DataFrame containing consumption data
                                                                      per year in liters with energy supply information.
        :type dataframe_consumption_per_km_liter_with_energy_supply: pd.DataFrame

        :param dataframe_consumption_per_km_kWh_with_energy_supply: A pandas DataFrame containing consumption data
                                                                   per year in kilowatt-hours (kWh) with energy supply information.
        :type dataframe_consumption_per_km_kWh_with_energy_supply: pd.DataFrame

        :param dataframe_with_co2e_values: A pandas DataFrame containing CO2e values and energy supply information.
        :type dataframe_with_co2e_values: pd.DataFrame

        :return: A pandas Series with calculated CO2e usage per car for each row in the input DataFrame.
        :rtype: pd.Series

        This function iterates through the rows in the input DataFrame (dataframe_with_co2e_values) and calculates
        the CO2e usage per car based on the provided consumption data and CO2e values. The resulting CO2e values
        are stored in a Series and returned.

        Note: The input DataFrames must have matching indices for this function to work correctly.
        """
    calculated_co2_series = pd.Series(index=dataframe_with_co2e_values.index)
    for ind in dataframe_with_co2e_values.index:
        row = dataframe_with_co2e_values.loc[ind]
        if row['energysupply'] == 'gasoline':
            calculated_co2e = dataframe_consumption_per_km_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_WtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_WtW'] + row['share_bioliq_totalgasoline'] * row['co2e_bioliq_WtW']+ row['share_ptl_totalgasoline'] * row['co2e_ptl_WtW'])
        elif row['energysupply'] == 'diesel':
            calculated_co2e = dataframe_consumption_per_km_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_D7_totaldiesel'] * row['co2e_D7_WtW'] + row['share_hvo_totaldiesel'] * row['co2e_hvo_WtW'])
        elif row['energysupply'] == 'battery':
            calculated_co2e = dataframe_consumption_per_km_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_WtW']
        elif row['energysupply'] == 'hybrid':
            calculated_co2e = dataframe_consumption_per_km_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_WtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_WtW']) + dataframe_consumption_per_km_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_WtW']
        else:
            calculated_co2e = None
        calculated_co2_series[ind] = calculated_co2e
    return calculated_co2_series


def get_co2e_usage_wtw_per_car(dataframe_consumption_per_year_liter_with_energy_supply, dataframe_consumption_per_year_kWh_with_energy_supply,  dataframe_with_co2e_values):
    """
        Calculate the CO2 equivalent (CO2e) usage per car based on consumption data and CO2e values.

        :param dataframe_consumption_per_year_liter_with_energy_supply: A pandas DataFrame containing consumption data
                                                                      per year in liters with energy supply information.
        :type dataframe_consumption_per_year_liter_with_energy_supply: pd.DataFrame

        :param dataframe_consumption_per_year_kWh_with_energy_supply: A pandas DataFrame containing consumption data
                                                                   per year in kilowatt-hours (kWh) with energy supply information.
        :type dataframe_consumption_per_year_kWh_with_energy_supply: pd.DataFrame

        :param dataframe_with_co2e_values: A pandas DataFrame containing CO2e values and energy supply information.
        :type dataframe_with_co2e_values: pd.DataFrame

        :return: A pandas Series with calculated CO2e usage per car for each row in the input DataFrame.
        :rtype: pd.Series

        This function iterates through the rows in the input DataFrame (dataframe_with_co2e_values) and calculates
        the CO2e usage per car based on the provided consumption data and CO2e values. The resulting CO2e values
        are stored in a Series and returned.

        Note: The input DataFrames must have matching indices for this function to work correctly.
        """
    calculated_co2_series = pd.Series(index=dataframe_with_co2e_values.index)
    for ind in dataframe_with_co2e_values.index:
        row = dataframe_with_co2e_values.loc[ind]
        if row['energysupply'] == 'gasoline':
            calculated_co2e = dataframe_consumption_per_year_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_WtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_WtW'] + row['share_bioliq_totalgasoline'] * row['co2e_bioliq_WtW']+ row['share_ptl_totalgasoline'] * row['co2e_ptl_WtW'])
        elif row['energysupply'] == 'diesel':
            calculated_co2e = dataframe_consumption_per_year_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_D7_totaldiesel'] * row['co2e_D7_WtW'] + row['share_hvo_totaldiesel'] * row['co2e_hvo_WtW'])
        elif row['energysupply'] == 'battery':
            calculated_co2e = dataframe_consumption_per_year_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_WtW']
        elif row['energysupply'] == 'hybrid':
            calculated_co2e = dataframe_consumption_per_year_liter_with_energy_supply['consumption_manufacturer_l'][ind] * (row['share_E5_totalgasoline'] * row['co2e_E5_WtW'] + row['share_E10_totalgasoline'] * row['co2e_E10_WtW']) + dataframe_consumption_per_year_kWh_with_energy_supply['consumption_manufacturer_kWh'][ind] * row['co2e_electricity_WtW']
        else:
            calculated_co2e = None
        calculated_co2_series[ind] = calculated_co2e
    return calculated_co2_series


def get_co2e_usage_wtw_per_segment(series_with_calculated_co2e, dataframe_with_vehicle_stock):
    """
        Calculate the CO2 equivalent (CO2e) usage per segment based on calculated CO2e values and vehicle stock data.

        :param series_with_calculated_co2e: A pandas Series with calculated CO2e values, where the index
                                             corresponds to segments.
        :type series_with_calculated_co2e: pd.Series

        :param dataframe_with_vehicle_stock: A pandas DataFrame containing information about vehicle stock,
                                             where each row represents a segment and includes at least a 'vehicle_stock' column.
        :type dataframe_with_vehicle_stock: pd.DataFrame

        :return: A pandas Series with calculated CO2e usage per segment, where the index corresponds to the segments
                 in the input DataFrame.
        :rtype: pd.Series

        This function iterates through the segments in the input DataFrame and calculates the CO2e usage per segment
        based on the provided CO2e values and vehicle stock data. The resulting CO2e values are stored in a Series
        and returned.

        Note: The input Series and DataFrame must have matching indices for this function to work correctly.
        """
    calculated_co2e_per_segment_series = pd.Series(index=dataframe_with_vehicle_stock.index)
    for ind in dataframe_with_vehicle_stock.index:
        row = dataframe_with_vehicle_stock.loc[ind]
        calculated_co2e_per_segment = series_with_calculated_co2e[ind] * row['number_of_cars_in_segment']
        calculated_co2e_per_segment_series[ind] = calculated_co2e_per_segment
    return calculated_co2e_per_segment_series


def calculate_production_co2e_per_car(dataframe):
    """
       Calculate the CO2 equivalent (CO2e) emissions during the production phase per car.

       :param dataframe: A pandas DataFrame containing information about car production factors,
                         such as glider weight, electric engine power, battery capacity, and more.
       :type dataframe: pd.DataFrame

       :return: A pandas Series with calculated CO2e emissions during the production phase per car,
                where the index corresponds to the rows in the input DataFrame.
       :rtype: pd.Series

       This function iterates through the rows in the input DataFrame and calculates the CO2e emissions during the
       production phase per car based on the provided production factors. The resulting CO2e values are stored in
       a Series and returned.

       Note: The input DataFrame should contain relevant columns like 'glider_weight', 'power_electric_engine',
       'power_electric_engine_2', 'battery_capacity_brutto', 'co2e_production', 'co2e_electric_engine',
       'weight_electric_drivechain', 'co2e_drivechain', etc.
       """
    calculated_co2e_production_series = pd.Series(index=dataframe.index)
    for ind in dataframe.index:
        row = dataframe.loc[ind]
        calculated_co2e_production = row['glider_weight'] * row['co2e_production'] + (row['power_electric_engine'] + row['power_electric_engine_2'])*row['co2e_electric_engine'] + row['battery_capacity_brutto']*row['co2e_battery_production'] + row['weight_electric_drivechain']*row['co2e_drivechain']
        calculated_co2e_production_series[ind] = calculated_co2e_production
    return calculated_co2e_production_series


def calculate_production_co2e_per_vehicle_class(series_production_co2e_per_car, dataframe):
    production_co2e_per_segment_series = pd.Series(index=dataframe.index)
    for ind in dataframe.index:
        row = dataframe.loc[ind]
        production_co2e_per_segment = series_production_co2e_per_car[ind] * row['number_of_cars_in_segment']
        production_co2e_per_segment_series[ind] = production_co2e_per_segment
    calculated_co2e_production_per_vehicle_class_icev = production_co2e_per_segment_series.loc['icev'].sum()
    calculated_co2e_production_per_vehicle_class_hev = production_co2e_per_segment_series.loc['hev'].sum()
    calculated_co2e_production_per_vehicle_class_phev = production_co2e_per_segment_series.loc['phev'].sum()
    calculated_co2e_production_per_vehicle_class_bev = production_co2e_per_segment_series.loc['bev'].sum()
    data = {'icev': calculated_co2e_production_per_vehicle_class_icev,
            'hev': calculated_co2e_production_per_vehicle_class_hev,
            'phev': calculated_co2e_production_per_vehicle_class_phev,
            'bev': calculated_co2e_production_per_vehicle_class_bev}
    calculated_co2e_production_per_vehicle_class_all_series = pd.Series(data=data, index=['icev', 'hev', 'phev', 'bev'])
    return calculated_co2e_production_per_vehicle_class_all_series


def calculate_co2e_savings(dataframe):
    """
       Calculate the CO2 equivalent (CO2e) savings based on glider and battery weight factors.

       :param dataframe: A pandas DataFrame containing information about CO2e savings factors, including glider weight,
                         battery weight, and associated CO2e savings.
       :type dataframe: pd.DataFrame

       :return: A pandas Series with calculated CO2e savings, where the index corresponds to the rows in the input DataFrame.
       :rtype: pd.Series

       This function iterates through the rows in the input DataFrame and calculates the CO2e savings based on the provided
       glider weight, battery weight, and associated CO2e savings factors. The resulting CO2e savings values are stored
       in a Series and returned.

       Note: The input DataFrame should contain relevant columns like 'glider_weight', 'co2e_savings_glider',
       'battery_weight', 'co2e_savings_battery', etc.
       """
    calculated_co2e_savings_series = pd.Series(index=dataframe.index)
    for ind in dataframe.index:
        row = dataframe.loc[ind]
        calculated_co2e_savings = row['glider_weight'] * row['co2e_savings_glider'] + row['battery_weight']*row['co2e_savings_battery']
        calculated_co2e_savings_series[ind] = calculated_co2e_savings
        # print(f"recycling aus calculations:{calculated_co2e_savings_series}")
    return calculated_co2e_savings_series


def calc_quadratic_regression(x, y, x_new):
    """
           Calculate the regression line for the co2e per year from 2020 until 2050.

           :param x: an array containing the years

           :type x: numpy.array

           :param y: an array containing the values matching the years from the x-array

           :type y: numpy.array

           :param x_new: the starting and end year and the stepsize
           :type x_new:

           :return y_new: an array containing all the newly calculated values
           :rtype: pd.Series

           This function is a regression function for calculating the co2e of different years because we only have the co2e of the year 2030 and 2045.

           Note: At this time the regression is a quadratic regression however the input values are a linear regression so this might have to change in the future depending on the given scenario.
           """
    plt.plot(x, y)
    # plt.show()

    # polynom approximation
    [a, b, c] = numpy.polyfit(x=x, y=y, deg=2)
    y_new = a * x_new[:] ** 2 + b * x_new[:] + c
    plt.plot(x_new, y_new)
    # plt.show()
    # polynom approximation
    # vectorized calculation for entire array
    return y_new


def get_unique_values_from_dict(data, key_of_interest, condition_dict=None):
    unique_values = set()

    for obj in data:
        if key_of_interest in obj:
            if condition_dict is None or all(obj.get(key, None) == value for key, value in condition_dict.items()):
                unique_values.add(obj[key_of_interest])
    return sorted(list(unique_values))


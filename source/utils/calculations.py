import pandas as pd
import numpy as np


def print_df(df_data: pd.DataFrame):
    print("I will print your dataframe:")
    print(df_data.to_string())
    print("DF printed!")


def get_vehicle_class(df_data: pd.DataFrame):
    vehicle_class_list = df_data.index.get_level_values(0).unique()
    vehicle_class_list = vehicle_class_list.drop(labels=['Quelle ', 'description', '2035'])
    print(f"vehicle_class_list: {vehicle_class_list}")
    return vehicle_class_list


def show_consumption_manufacturer(df_data: pd.DataFrame):
    for vehicle_class in get_vehicle_class(df_data):
        segments_per_vehicle_class = df_data.loc[vehicle_class]
        print(f"all vehicle classes and their segments: {segments_per_vehicle_class}")


'''
## consumption per segment per vehicle class
for vehicle_class in vehicle_class_list:
    df4 = selected_scenario_raw_data.loc[vehicle_class]
    print(f"sum: {np.sum(df4['vehicle_stock_icev_per_segment'])}")
    print(f"division: {df4['vehicle_stock_icev_per_segment']/100}")
'''

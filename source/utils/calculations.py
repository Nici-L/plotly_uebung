import pandas as pd


# todo: berechnungsmethoden schreiben statt aufrufe methoden, 2. methode berechne anteile an kraftstoffart,
# 3. Methode berechne co2e von kraftstoff dazu, überlege dir, ob nur mit series arbeiten sinn macht oder du ein dataframe brauchst und wenn ja, ob eine methode dafür sinnvoll ist ß

def calculate_yearly_consumption_liter(df_data):
    consumption_manufacturer_liter_per_km = df_data['consumption_manufacturer_l']/100
    consumption_manufacturer_liter_per_year = consumption_manufacturer_liter_per_km * df_data['mileage']
    return consumption_manufacturer_liter_per_year


def calculate_yearly_consumption_kwh(df_data):
    consumption_manufacturer_kwh_per_km = df_data['consumption_manufacturer_kWh']/100
    consumption_manufacturer_kwh_per_year = consumption_manufacturer_kwh_per_km * df_data['mileage']
    return consumption_manufacturer_kwh_per_year



def get_vehicle_class(df_data: pd.DataFrame):
    vehicle_class_list = df_data.index.get_level_values(0).unique()
    print(f"vehicle_class_list: {vehicle_class_list}")
    return vehicle_class_list


def get_segments_per_vehicle_class(df_data: pd.DataFrame):
    for vehicle_class in get_vehicle_class(df_data):
        segments_per_vehicle_class = df_data.loc[vehicle_class]
        print(f"all vehicle classes and their segments: {segments_per_vehicle_class}")
    return segments_per_vehicle_class
    # only last for loop is being saved and will remain the index for following calculations


def get_consumption_per_year(consumption_per_100km, df_data):
    consumption_per_km = consumption_per_100km/100
    consumption_per_year = consumption_per_km*df_data['mileage']
    return consumption_per_year


def get_co2e_usage_ttw_per_car(dataframe_consumption_liter, dataframe_consumption_kwh,  dataframe_og):
    calculate_co2e_gasoline_list = []
    for ind in dataframe_og.index:
        row = dataframe_og.loc[ind]
        if row['energysupply'] == 'gasoline':
            calculate_co2e_gasoline = dataframe_consumption_liter['consumption_manufacturer_l'][ind] * (dataframe_og['share_E5_totalgasoline'][ind] * dataframe_og['co2e_E5_TtW'][ind] + dataframe_og['share_E10_totalgasoline'][ind] * dataframe_og['co2e_E10_TtW'][ind])
            calculate_co2e_gasoline_list.append(calculate_co2e_gasoline)
            print(f"calculate_co2e_gasoline_list: {calculate_co2e_gasoline_list}")
        elif row['energysupply'] == 'diesel':
            calculate_co2e_diesel = dataframe_consumption_liter['consumption_manufacturer_l'][ind] * (dataframe_og['share_D7_totaldiesel'] * dataframe_og['co2e_D7_TtW']) #+ dataframe_og['share_hvo_totaldiesel'] * dataframe_og['co2e_hvo_TtW'])
        elif row['energysupply'] == 'battery':
            calculate_co2e_elecricity = dataframe_consumption_kwh['consumption_manufacturer_kWh'][ind] #* (dataframe_og['share_elecricity_totaldiesel'] * dataframe_og['co2e_electricity_TtW'])

    return calculate_co2e_gasoline, calculate_co2e_diesel, calculate_co2e_elecricity

## todo: methode fertig, liste für alles, excel daten ergänzen, testen ob liste für grafik benutzt werden kann, für gesamtfahrzeuge machen, nächste methode


'''def combine_consumptions(consumption1, consumption2, df_data):
    combined_consumptions = consumption1.combine_first(consumption2)
    combined_consumptions_order = combined_consumptions.reindex_like(df_data)
    return combined_consumptions_order'''





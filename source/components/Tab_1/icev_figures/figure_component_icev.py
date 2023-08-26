import numpy
import plotly.express as px
import pandas as pd
import math
import plotly.graph_objects as go

df = pd.read_csv('source/assets/icev_co2e_2022_py.CSV', sep=';', decimal=",", thousands='.', encoding="ISO-8859-1")

# caps if it is a constant
# icev
co2e_vehicle_production_per_kg = 7.2
co2e_savings_recycling_vehicle = -2.93 * df['average vehicle weight 2022']
co2e_per_liter_gasoline_ttw = 2.3
co2e_per_liter_gasoline_wtw = 2.8
co2e_per_liter_diesel_wtw = 3.15
co2e_icev_vehicle_production = df['average vehicle weight 2022'] * co2e_vehicle_production_per_kg

# Filters rows with gasoline consumption
gasoline_segments = df[df['gasoline consumption manufacturer'].notnull()]
gasoline_consumption_per_km = gasoline_segments['gasoline consumption manufacturer']/100
yearly_gasoline_consumption = df['mileage year 2022'] * gasoline_consumption_per_km
co2e_gasoline_usage_per_year = yearly_gasoline_consumption * co2e_per_liter_gasoline_ttw
co2e_gasoline_usage_per_year_whole_segment = (gasoline_segments['vehicle stock 2022'] * co2e_gasoline_usage_per_year)


# Filters rows with diesel consumption
diesel_segments = df[df['diesel consumption manufacturer'].notnull()]
diesel_consumption_per_km = diesel_segments['diesel consumption manufacturer']/100
yearly_diesel_consumption = df['mileage year 2022'] * diesel_consumption_per_km
co2e_diesel_usage_per_year = yearly_diesel_consumption * co2e_per_liter_diesel_wtw
co2e_diesel_usage_per_year_whole_segment = (diesel_segments['vehicle stock 2022'] * co2e_diesel_usage_per_year)  # is a list containing 12 values, the NaN values are the ones in the gasoline list


# Merge gasoline and diesel co2e lists
merged_list_co2_usage_gas_and_diesel = []

for gas_val, diesel_val in zip(co2e_gasoline_usage_per_year_whole_segment, co2e_diesel_usage_per_year_whole_segment):
    if not math.isnan(gas_val):
        merged_list_co2_usage_gas_and_diesel.append(gas_val)
    elif not math.isnan(diesel_val):
        merged_list_co2_usage_gas_and_diesel.append(diesel_val)
    else:
        merged_list_co2_usage_gas_and_diesel.append(float('NaN'))

#merged_list_co2_usage_gas_and_diesel_int = list(map(int, merged_list_co2_usage_gas_and_diesel_float))
# merged_list_co2_usage_gas_and_diesel = merged_list_co2_usage_gas_and_diesel_int * (10 ** (-9))
#a = numpy.array(merged_list_co2_usage_gas_and_diesel_int)

# Merge gasoline and diesel co2e list for one car per segment
merged_list_co2_usage_gas_and_diesel_one_car = []

for gas_val, diesel_val in zip(co2e_gasoline_usage_per_year, co2e_diesel_usage_per_year):
    if not math.isnan(gas_val):
        merged_list_co2_usage_gas_and_diesel_one_car.append(gas_val)
    elif not math.isnan(diesel_val):
        merged_list_co2_usage_gas_and_diesel_one_car.append(diesel_val)
    else:
        merged_list_co2_usage_gas_and_diesel_one_car.append(float('NaN'))


### plotly express figure
co2e_segments_icev_2023_barchart_horiz = px.bar(
    data_frame=df,
    x=[co2e_icev_vehicle_production, merged_list_co2_usage_gas_and_diesel_one_car],
    y='segments',
    orientation='h',
    barmode='stack',
    labels={'segments': 'Different vehicle segments as defined by the KBA ',
            'variable': 'lifecycle steps',
            'wide_variable_0': 'production',
            'x': 'usage'
            },
    title='CO2e of different vehicle segments in kg',
    text_auto='production',
    width=1300,
    height=600,
    template='plotly',
    color_discrete_map={
        'production': 'pink',
        'usage': 'lightblue'
    }
).update_layout(
    plot_bgcolor='#002b36',  # color Solar stylesheet
    paper_bgcolor='#002b36',
    font_color='white',
    barmode='relative',
    autosize=True,
).update_traces(
    cliponaxis=True,
    texttemplate="%{x:.2s}",
)


### plotly graph_object figure
barchart_horizontal_test = go.Figure(
    data=[
        go.Bar(
            x=co2e_icev_vehicle_production,
            y=df["segments"],
            textposition="auto",
            name="production",
            # yaxis="y1",
            orientation='h',
            #  marker_color=column["color"],
        ),
        go.Bar(
            x=merged_list_co2_usage_gas_and_diesel_one_car,
            y=df["segments"],
            textposition="auto",
            name="usage",
            # yaxis="y1",
            orientation='h',
            #  marker_color=column["color"],
        ),
        go.Bar(
            x=co2e_savings_recycling_vehicle,
            y=df["segments"],
            textposition="auto",
            name="recycling",
            # yaxis="y1",
            orientation='h',
            # marker_color=column["color"],
                 ),
    ],
    layout={  # dictionary 'key':'value'
        'barmode': 'relative',
        'title': 'CO2e of different vehicle segments in kg',
        'template': 'ggplot2',
        'plot_bgcolor': '#002b36',  # color Solar stylesheet
        'paper_bgcolor': '#002b36',
        'font_color': 'white',
        # 'yaxis':{'categoryorder': 'array', 'categoryarray': ['Mittelklasse','Kompaktklasse','Kleinwagen','Mini']},
    }
)
barchart_horizontal_test.update_layout(
    barmode='relative',
    title='CO2e of different vehicle segments in kg',
    # width=800,
    # height=450,
    template='ggplot2',
    plot_bgcolor='#002b36',  # color Solar stylesheet
    paper_bgcolor='#002b36',
    font_color='white',
)


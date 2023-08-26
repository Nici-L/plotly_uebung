import plotly.express as px
import source.components.Tab_1.icev_figures.figure_component_icev as icev
import numpy as np
import pandas as pd

co2e_passenger_cars_own_calc_2022 = np.sum(icev.merged_list_co2_usage_gas_and_diesel)
co2e_passenger_cars_2022 = 91.742
co2e_passenger_cars_2025 = 81.18
co2e_passenger_cars_2030 = 56.1

columns = ["co2e_passenger_cars_own_calc_2022", "co2e_passenger_cars_2022", "co2e_passenger_cars_2025", "co2e_passenger_cars_2030"]

data = [
    [co2e_passenger_cars_own_calc_2022, co2e_passenger_cars_2022, co2e_passenger_cars_2025, co2e_passenger_cars_2030]
]

df_co2e_pass_cars = pd.DataFrame(data, columns=columns)

data = {
    "CO2 Emission in mio t": {
        "CO2e Passenger Cars (Own Calc) 2022": 87.5,
        "CO2e Passenger Cars 2022": 91.74,
        "CO2e Passenger Cars 2025": 81.18,
        "CO2e Passenger Cars 2030": 56.1
    }
}

# Create the DataFrame from the dictionary and set the table header
df_co2e_pass_cars = pd.DataFrame(data)
df_co2e_pass_cars.index.name = "Year"  # Add a name for the row index (optional)


co2e_passenger_cars_barchart_horiz = px.bar(
    data_frame=df_co2e_pass_cars,
    x='CO2 Emission in mio t',
    orientation='h',
    barmode='relative',
    title='CO2e of passenger cars per year',
    text_auto=True,
    width=1100,
    height=400,
    template='plotly'
).update_layout(
    plot_bgcolor='#002b36',  # color Solar stylesheet
    paper_bgcolor='#002b36',
    font_color='white',
    barmode='relative',
    autosize=True,
).update_traces(
    cliponaxis=True
)

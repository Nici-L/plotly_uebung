import numpy
import plotly.express as px
import pandas as pd
import math
import plotly.graph_objects as go


### plotly express figure
'''
co2e_segments_icev_2023_barchart_horiz = px.bar(
    data_frame=,
    x=[],
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
'''


'''
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
'''
'''
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

'''
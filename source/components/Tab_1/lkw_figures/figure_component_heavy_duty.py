import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


df_lkw = pd.read_csv('source/assets/lkw_co2e_icev_2022_csv.csv', sep=';', decimal=",", thousands='.', encoding="ISO-8859-1")


### plotly graph_object figure
barchart_horizontal_test_lkw = go.Figure(
    data=[
        go.Bar(
            x=df_lkw['Herstellung [kg CO2e]'],
            y=df_lkw["LKW Segment"],
            textposition="auto",
            name="production",
            # yaxis="y1",
            orientation='h',
            #  marker_color=column["color"],
        ),
        go.Bar(
            x=df_lkw['WtW Kraftstoff B7 [kg CO2e]'],
            y=df_lkw["LKW Segment"],
            textposition="auto",
            name="usage",
            # yaxis="y1",
            orientation='h',
            #  marker_color=column["color"],
        ),
        go.Bar(
            x=df_lkw['Herstellung AdBlue  [kg CO2e]'],
            y=df_lkw["LKW Segment"],
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
barchart_horizontal_test_lkw.update_layout(
    barmode='relative',
    title='CO2e of different vehicle segments in kg',
    template='ggplot2',
    plot_bgcolor='#002b36',  # color Solar stylesheet
    paper_bgcolor='#002b36',
    font_color='white',
)

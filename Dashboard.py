#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np
import geopandas as gpd
import pandas as pd
import json


# In[19]:


import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


# In[20]:


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
app = Dash("Mexpob", external_stylesheets=external_stylesheets)
server = app.server

# In[21]:


url1= 'https://raw.githubusercontent.com/adogus11/portafolio/main/datos/estadospob.geojson'
gdf = gpd.read_file(url1)
nuevos_nombres = {'POB': 'Population', 'ALF': 'Illiterate rate', 'DMP': 'Unemployment rate',
                   'HXV':'Average number of people per household', 'AGE':'Average age'}
gdf = gdf.rename(columns=nuevos_nombres)
url2= 'https://raw.githubusercontent.com/adogus11/portafolio/main/datos/Ciudadespoblaci%C3%B3n.geojson'
gdfp = gpd.read_file(url2)
gdfp['Población'] = gdfp['Población'].astype(float)


# In[22]:


url3 = 'https://raw.githubusercontent.com/adogus11/portafolio/main/datos/IDB.csv'
df= pd.read_csv(url3)
df= df.dropna()
df = df.replace('..', np.nan)
df_w = df.pivot(index=['Country Name', 'Country Code'], columns='Series Code', values='2019 [YR2019]')
df_w.reset_index(inplace=True)
df_w1 = df_w
df_w1['EN.POP.DNST'] = df_w1['EN.POP.DNST'].astype(float)
df_w1['EN.URB.LCTY'] = df_w1['EN.URB.LCTY'].astype(float)
df_w1['SL.UEM.TOTL.NE.ZS'] = df_w1['SL.UEM.TOTL.NE.ZS'].astype(float)
df_w1['SP.POP.TOTL'] = df_w1['SP.POP.TOTL'].astype(float)
outsiders = ['MLT','MDV','BHR','GIB','HKG','SGP','MCO','MAC']
df_w1 = df_w1[~df_w1['Country Code'].isin(outsiders)]
nuevos_nombres_w = {'SP.POP.TOTL': 'Population', 'SL.UEM.TOTL.NE.ZS': 'Unemployment(% of total labor force)',
                    'EN.URB.LCTY': 'Population in largest city',
                    'EN.POP.DNST':'Population density'} 
df_w1 = df_w1.rename(columns=nuevos_nombres_w)


# In[23]:


app.layout = html.Div (children=[
    html.H1(children='Population statistics in maps (Dashbord demo with python)',
            style = {'text-align':'center', 
                    'background-color': '#FACC90',
                    'height': '70px',
                    'border-radius': '30px 30px'}),
    html.Br(),
    html.H3(children='Map of Mexico (Select topic)'),
    html.Div([dcc.Dropdown(id='slt_opt',
                           options=[
        {'label':'Population', 'value': 'Population'},
        {'label':'Illiterate rate', 'value': 'Illiterate rate'},
        {'label':'Unemployment rate', 'value': 'Unemployment rate'}, 
        {'label':'Average number of people per household', 'value': 'Average number of people per household'},
        {'label':'Average age', 'value': 'Average age'},                       
    ],
        value = 'Population',
        style = {'font-size': '18px', 'width':'50%','align-items': 'center'}),
        html.Div(id='dd-output-container')
    ],
    style={'align-items': 'center'},
            ),
    html.Div(id='output_container', children=[], style = {'font-size': '14px'}),
    html.Br(),
    dcc.Graph(id='mapa', figure={}, style = {'background-color': '#74ADDB'}),
    html.Br(),
    html.H3(children='Map of the World (Select topic)'),
    html.Div([dcc.Dropdown(id='slt_opt1',
                           options=[
        {'label':'Population', 'value': 'Population'},
        {'label':'Unemployment(% of total labor force)', 'value': 'Unemployment(% of total labor force)'},
        {'label':'Population in largest city', 'value': 'Population in largest city'}, 
        {'label':'Population density', 'value': 'Population density'},                    
    ],
        value = 'Population',
        style = {'font-size': '18px', 'width':'50%','align-items': 'center'}),
        html.Div(id='dd-output-container1')
    ]),
    html.Div(id='output_container1', children=[], style = {'font-size': '14px'}),
    html.Br(),
    dcc.Graph(id='mapa1', figure={}),
    html.Br(),
    html.H3(children="Most populated cities in Mexico", style = {'text-align':'center', 'Padding': '5%',}),
    html.Br(),
    dcc.Graph(id='mapa2', figure={}),
    html.Br(),
    html.Div([
        html.Div(["© 2023 My Dash demo", html.Br(), "Gustavo Adolfo Islas Cadena"], style={'text-align': 'center'}),
    ], style={'background-color': '#FACC90', 'padding': '10px'})
], style = {'background-color': '#74ADDB', 'padding':'0% 2%'})


@app.callback(
    [Output(component_id = 'output_container', component_property='children'),
    Output(component_id = 'mapa', component_property='figure'),
    Output(component_id = 'output_container1', component_property='children'),
    Output(component_id = 'mapa1', component_property='figure'),
    Output(component_id = 'mapa2', component_property='figure')],
    [Input(component_id = 'slt_opt', component_property='value'),
     Input(component_id = 'slt_opt1', component_property='value')
    ]
)

def update(op_slt,op_slt1):
    container= 'The range chosen by user was: {}'.format(op_slt)
    
    fig = px.choropleth(gdf,
                   geojson=gdf.geometry,
                   locations=gdf.index,
                   color=op_slt,
                   title= '{}'.format(op_slt),
                   projection="mercator",
                   labels={'index':'State',op_slt:'Value'}
                   )
    
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    fig.update_layout(
    plot_bgcolor='lightgray',  
    paper_bgcolor='lightgray'  
)
    
    container1= 'The range chosen by user was: {}'.format(op_slt1)
    
    
    fig1 = px.choropleth(df_w1, locations='Country Code', locationmode='ISO-3', color=op_slt1,
                           color_continuous_scale="Viridis",
                           scope="world",
                           title= '{}'.format(op_slt1),
                           labels={'Country Code':'Country',op_slt1:'Value'}
                          )
    fig1.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    fig1.update_layout(
    plot_bgcolor='lightgray',  
    paper_bgcolor='lightgray'  
)    
    fig2 = px.scatter_mapbox(gdfp, color="name",
                     lat= gdfp['geometry'].y, lon=gdfp['geometry'].x,
                     hover_name="name", size="Población",
                     mapbox_style= 'carto-positron',
                     center= {"lat": 23.6345,"lon": -102.5528},
                     zoom= 2,
                     labels= {'name':'City', 'Población':'Population'})
    fig2.update_layout(margin={"r":30,"t":30,"l":50,"b":30})
    #fig2.update_geos(fitbounds="locations", visible=True)
    fig2.update_layout(
    plot_bgcolor='lightgray',  
    paper_bgcolor='lightgray',
)

    return container, fig, container1, fig1, fig2


# In[24]:


if __name__ == 'Mexpob':
    app.run(host='0.0.0.0', port=10000)


# In[ ]:





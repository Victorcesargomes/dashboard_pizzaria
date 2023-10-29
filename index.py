from dash import html, dcc 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.express as px

from app import app
from _map import *
from _histogram import *
from _controllers import *

# ========================================= #
# Load Data #
df = pd.read_csv('Pizzaria_clientes.csv')

# Usar a latitude e longitude média (a ideia é centralizar o mapa)
mean_lat = df['Latitude'].mean()
mean_long = df['Longitude'].mean()






app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([controlers], md=3),
            dbc.Col([map, hist], md=9),
        ])

    ], fluid=True, )



# ==================
# callbacks
# =================
@app.callback([Output('hist-graph', 'figure'), Output('map-graph', 'figure')],
              [Input('location-dropdown', 'value'),
               Input('slider-square-size', 'value'),
               Input('dropdown-color', 'value')])
def update_hist(location, square_size, color_map):
    if location is None:
        df_intermediate = df.copy()
    else:
        df_intermediate = df[df['Cidades'] == location] if location != 0 else df.copy()
    
        size_limit = slider_size[square_size] if square_size is not None else df['Quantidade'].max()
        df_intermediate = df_intermediate[df_intermediate["Quantidade"] <= size_limit]

    hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)
    hist_layout = go.Layout(
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend = False,
        template = "plotly_dark",
        paper_bgcolor = "rgba(0, 0, 0,0 )")
    hist_fig.layout = hist_layout


    px.set_mapbox_access_token(open("keys/mapbox_key").read())


    map_fig = px.scatter_mapbox(df_intermediate, lat="Latitude", lon="Longitude", color=color_map,
                                size="Compras", size_max=15, zoom=10, opacity=0.9, color_continuous_scale='darkmint')
    
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat, lon=mean_long)),
                          template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)",
                          margin=go.layout.Margin(l=10, r=10, t=10, b=10))



    return hist_fig, map_fig



if __name__ == '__main__':
    app.run_server(debug=False)
    #app.run_server(host="0.0.0.0", port="8053") #para que o app rode na rede local
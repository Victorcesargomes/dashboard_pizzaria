# app.py
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Criar instância do aplicativo Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.scripts.config.serve_locally = True

# Load Data
df = pd.read_csv(r"assets/Pizzaria_clientes.csv")
mean_lat = df['Latitude'].mean()
mean_long = df['Longitude'].mean()

# ==========================
# _controller.py
# ==========================
list_of_locations = {
    "Todas": 0,
    "Abreu e Lima": 1,
    "Igarassu": 2,
    "Paulista": 3
}

slider_size = [1, 2, 3, 4, 5, 6, 7, 8]

controlers = dbc.Row([
    html.Img(id="logo", src=app.get_asset_url("logo2_dw.png"), style={"width": "70%"}),
    html.H1("Gestão de Relacionamento com o Cliente", style={"margin-top": "10px", "color": "white"}),
    html.P("""Utilize este dashboard para analisar e compreender o perfil de cada cliente, características, total de compras no mês, bem como a quantidade de pizzas compradas"""),

    html.H2("""Cidade""", style={"margin-top": "30px", "margin-bottom": "25px", "color": "white", "width": "50%"}),
    dcc.Dropdown(
        id="location-dropdown",
        options= [{"label": i, "value": j} for i, j in list_of_locations.items()],
        value=0,
        placeholder="Selecione uma cidade"
    ),
    html.H2("""Quantidade de Pizzas Compradas""", style={"margin-top": "40px", "margin-bottom": "20px", "color": "white"}),

    dcc.Slider(min=0, max=7, id="slider-square-size",
               marks={i: str(j) for i, j in enumerate(slider_size)}),

    html.H2("""Variável de Controle""",style={"margin-top": "40px", "margin-bottom": "20px", "color": "white"}),

    dcc.Dropdown(
        options=[{'label':'Compras', 'value': 'Compras'},
                 {'label': 'Idade', 'value': 'Idade'},
                 {'label': 'Sexo', 'value': 'Sexo'},
                 {'label': 'Cliente', 'value':'Cliente'},
                 ],
                 value='Compras',
                 id="dropdown-color"
    )
])

# ==========================
# _histogram.py
# ==========================
fig_hist = go.Figure()

fig_hist.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)")

hist = dbc.Row([
    dcc.Graph(id="hist-graph", figure=fig_hist)
], style={"height": "20vh"})

# ==========================
# _map.py
# ==========================
fig_map = go.Figure()

fig_map.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)")

map_ = dbc.Row([
    dcc.Graph(id="map-graph", figure=fig_map)
], style={"height": "80vh"})

# ==========================
# index.py
# ==========================
app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([controlers], md=3),
            dbc.Col([map_, hist], md=9),
        ])
    ], fluid=True,
)

# ==========================
# Callbacks
# ==========================
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
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor="rgba(0, 0, 0,0 )")
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
     #app.run_server(host="0.0.0.0", port="8053")  # para que o app rode na rede local

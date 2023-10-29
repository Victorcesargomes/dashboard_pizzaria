from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app

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


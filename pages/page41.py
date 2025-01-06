from dash import html, dcc, Input, Output, Dash, callback
import dash_bootstrap_components as dbc
import pandas as pd



df = pd.read_excel("assets/Acumulados.xlsx")

layout = dbc.Container([
    html.H1("Resumen de jugadores por equipos", className='text-center my-4'),

    ####Dropdown para seleccion de Equipo
    dbc.Row([
        dbc.Col([
            html.Label("Selecciona un equipo", className='form-label'),
            dcc.Dropdown(
                id='dropdown-team',
                options=[
                    {'label':equipo, 'value':equipo}
                    for equipo in df['Team'].unique()
                    ],
                placeholder="Selecciona un equipo",
                className="mb-3"


            ),


        ], width=6),

        dbc.Col([
            html.Img(
                id='team-logo',
                style={
                    'width': '100%', 
                    'height': 'auto', 
                    'max-height': '150px', 
                    'object-fit': 'contain'
                },
                className="mb-3"
            )
        ], width=6, class_name="text-center"),
 

    ]),

    ##############Dropdown para  jugadores
    dbc.Row([
        dbc.Col([
            html.Label("Selecciona un jugador", className='form-label'),
            dcc.Dropdown(
                id='dropdown-player',
                placeholder="Selecciona un jugador",
                className="mb-3"
            ),
        ], width=6)
    ]),

    #################### CARD PARA MÉTRICAs #################

    dbc.Row([
        dbc.Col(dbc.Card(id='points-card',body=True, color='primary', inverse=True), width=3),
        dbc.Col(dbc.Card(id='rebound-card',body=True, color='info', inverse=True), width=3),
        dbc.Col(dbc.Card(id='assists-card',body=True, color='success', inverse=True), width=3),
        dbc.Col(dbc.Card(id='min-card',body=True, color='success', inverse=True), width=3),

    ], class_name="my-4")

    
], fluid=True)

##### CALLBACKS PARA ACTUALIZAR DROPDOWN DE JUGADORES#####
@callback(
    Output('dropdown-player', 'options'),
    Input('dropdown-team', 'value')
)

def update_players_dropdown(selected_team):
    if selected_team:
        #Filtrar jugadores del equipo seleccionado
        jugadores = df[df['Team']==selected_team]['Jugadores']
        return [{'label': jugador, 'value':jugador}for jugador in jugadores]
    return[] 

@callback(
    [Output('min-card', 'children'),
    Output('points-card', 'children'),
    Output('rebound-card', 'children'),
    Output('assists-card', 'children'),
    Input('dropdown-player', 'value')
    ]
)

def update_player_info(selected_player):
    if selected_player:
        #Filtrar datos del jugador seleccionado
        metricas = df[df['Jugadores']==selected_player].iloc[0]
        points = metricas['PTS']
        rebounds = metricas['RT']
        assists = metricas['AST']
        min = metricas['MIN']

        return (
            f"Minutos: {min}",
            f"Puntos: {points}",
            f"Rebotes: {rebounds}",
            f"Asistencias: {assists}"
        )
    return (
        "Minutos: N/A",
        "Puntos: N/A",
        "Rebotes: N/A",
        "Asistencias: N/A",
        )

# Actualizar logo del equipo
@callback(
    Output('team-logo', 'src'),
    Input('dropdown-team', 'value')
)
def update_team_logo(selected_team):
    if selected_team:
        # Ruta del logo
        return f"/assets/logos/{selected_team}.png"
    return "/assets/logos/default.png" 
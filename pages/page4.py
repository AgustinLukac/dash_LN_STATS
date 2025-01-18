from dash import html, dcc, Input, Output, Dash, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path


df = pd.read_excel("assets/Acumulados.xlsx")
df_1 = pd.read_excel("assets/boxscore_partidos.xlsx")

df_1['Fecha'] = pd.to_datetime(df_1['Fecha'], format='%d/%m/%Y', errors='coerce')
df_1 = df_1.sort_values(by='Fecha', ascending=True)

layout = dbc.Container([
    html.H1("Resumen de jugadores por equipos", className='text-center my-4'),

    #### Dropdown para selección de Equipo y contenedor del logo
    dbc.Row([
        # Columna para los dropdowns
        dbc.Col([
            html.Label("Selecciona un equipo", className='form-label'),
            dcc.Dropdown(
                id='dropdown-team',
                options=[
                    {'label': equipo, 'value': equipo}
                    for equipo in sorted(df['Team'].unique())
                ],
                placeholder="Selecciona un equipo",
                className="mb-3"
            ),
            html.Label("Selecciona un jugador", className='form-label'),
            dcc.Dropdown(
                id='dropdown-player',
                placeholder="Selecciona un jugador",
                className="mb-3"
            ),
            
        ], width=6),

        # Columna para el logo
        dbc.Col([
            html.Div(
                html.Img(
                    id='team-logo',
                    style={
                        'width': '100%', 
                        'height': 'auto', 
                        'max-height': '150px', 
                        'object-fit': 'contain'
                    }
                ),
                style={
                    #'border': '1px solid black', 
                    'padding': '10px', 
                    'text-align': 'center',
                    'height': '100%'  # Asegura que ocupe todo el espacio de la fila
                }
            )
        ], width=6)
    ]),

    #### Card para métricas
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([

                    html.P("Selecciona un equipo y un jugador para ver los datos", 
                    className="card-text text-center text-muted")  # Otro valor
                ]),
                id='points-card', 
                body=True, 
                color='primary', 
                inverse=True,
                className="card-text text-center"), width=3),


        dbc.Col(dbc.Card(id='rebound-card', body=True, color='info', inverse=True,className="card-text text-center"), width=3),
        dbc.Col(dbc.Card(id='assists-card', body=True, color='success', inverse=True,className="card-text text-center"), width=3),
        dbc.Col(dbc.Card(id='min-card', body=True, color='dark', inverse=True,className="card-text text-center"), width=3),
    ], class_name="my-4"),

    html.Div([
         html.H4("Gráficos de rendmientos por partido", className='text-center my-4'),

         dcc.Graph(id='graph_line'),
         dcc.DatePickerRange(id='selector_fecha',
                            start_date = df_1['Fecha'].min(),
                            end_date = df_1['Fecha'].max())


         
    ])
], fluid=True)

##### CALLBACKS #####

# Actualizar Dropdown de jugadores
@callback(
    Output('dropdown-player', 'options'),
    Input('dropdown-team', 'value')
)
def update_players_dropdown(selected_team):
    if selected_team:
        jugadores = df[df['Team'] == selected_team]['Jugadores']
        return [{'label': jugador, 'value': jugador} for jugador in jugadores]
    return []

# Actualizar métricas del jugador
@callback(
    [Output('rebound-card', 'children'),
     Output('assists-card', 'children'),
     Output('min-card', 'children'),
     Output('points-card', 'children'),],
    Input('dropdown-player', 'value')
)
def update_player_info(selected_player):
    if selected_player:
        metricas = df[df['Jugadores'] == selected_player].iloc[0]
        points = metricas['PTS']
        rebounds = metricas['RT']
        assists = metricas['AST']
        assists_p = metricas['AST %']
        min = metricas['MIN']
        fgm_3 = metricas['3FGM']
        fga_3 = metricas['3FGA']
        fga_3_p = metricas['3FG %']
        fga_2 = metricas['2FGA']
        fgm_2 = metricas['2FGM']
        fga_2_p = metricas['2FG %']
        fta = metricas['FTA']
        ftm = metricas['FTM']
        fta_p = metricas['FT %']
        to = metricas['TO']
        to_p = metricas['TO %']
        usg = metricas['USG %']
        plays = metricas['PLAYS']

        return (
            dbc.CardBody([
                html.H1("ANOTACIÓN",className="card-title text-center text-primary fw-bold mt-4 mb-4"),
                html.H2(f"Puntos: {points}", className="card-text text-center"),
                html.H4(f"T3: {fgm_3} / {fga_3} - {fga_3_p * 100:.1f} % ", className="card-text text-center"),
                html.H4(f"T2: {fgm_2} / {fga_2} - {fga_2_p * 100:.1f} % ", className="card-text text-center"),
                html.H4(f"T1: {ftm} / {fta} - {fta_p*100:.1f} % ", className="card-text text-center"),
            ]),
            dbc.CardBody([
                html.H1("POSESIÓN",className="card-title text-center text-white fw-bold mt-4 mb-4"),
                html.H2(f"MIN: {min}", className="card-text text-center"),
                html.H4(f"USG %: {usg* 100:.1f} - Plays: {plays}", className="card-text text-center"),
                html.H4(f"ASISTENCIAS: {assists} - {assists_p * 100:.1f} %", className="card-text text-center"),
                html.H4(f"TO: {to} - {to_p*100:.1f} % ", className="card-text text-center"),
            ]),
            f"Minutos: {min}",
            
            f"Rebotes: {rebounds}",
            
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
    return "/assets/logos/default.png"  # Imagen por defecto si no hay equipo seleccionado

@callback(Output('graph_line','figure'),
          [Input('selector_fecha','start_date'), 
           Input('selector_fecha','end_date'),
           Input('dropdown-player', 'value')])

def actualizar_graph(fecha_min, fecha_max, selected_player):
    filtered_df = df_1[(df_1['Fecha'] >= fecha_min) & (df_1['Fecha'] <= fecha_max)]

    if not selected_player:
        return {
            'data': [],
            'layout': go.Layout(
                title='Rendimiento por partido',
                xaxis={'title': 'Fecha'},
                yaxis={'title': 'Ptos'},
                annotations=[
                    {
                        'text': 'Selecciona un jugador para ver el gráfico',
                        'xref': 'paper',
                        'yref': 'paper',
                        'showarrow': False,
                        'font': {'size': 16}
                    }
                ]
            )
        }

    player_data = filtered_df[filtered_df['Jugadores'] == selected_player]
    promedio_puntos = player_data['PTS'].mean()

    # Crear la traza para el jugador
    trace = go.Scatter(
        x=player_data['Fecha'],
        y=player_data['PTS'],
        mode='lines+markers',
        marker={
            'size': 10,
            'color': player_data['Resultado'].map({'Gano': 'green', 'Perdio': 'red'}),
            'symbol': 'circle'
        },
        opacity=0.7,
        name=selected_player,
    )

    # Agregar los logos como imágenes
    images = []
    for _, row in player_data.iterrows():
        images.append({
            'source': f"/assets/logos/{row['Opp']}.png",
            'x': row['Fecha'],
            'y': row['PTS'] + 1,
            'xref': 'x',
            'yref': 'y',
            'xanchor': 'center',
            'yanchor': 'middle',
            'sizex': 0.5,  # Ajusta el tamaño
            'sizey': 0.5,  # Ajusta el tamaño
            'opacity': 1
        })

    # Crear la traza para la línea de promedio
    trace_avg = go.Scatter(
        x=player_data['Fecha'],
        y=[promedio_puntos] * len(player_data),
        mode='lines',
        line={'dash': 'dash', 'color': 'black'},
        opacity=0.5,
        name=f"Promedio: {promedio_puntos:.2f}"
    )

    return {
        'data': [trace, trace_avg],
        'layout': go.Layout(
            title='Rendimiento por partido',
            xaxis={'title': 'Fecha'},
            yaxis={'title': 'Ptos'},
            template='plotly_white',
            images=images  # Incluye las imágenes en el layout
        )
    }


from dash import html, dcc, Input, Output, Dash, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from pathlib import Path

# Cargar datos
df = pd.read_excel("assets/Acumulados.xlsx")
df_1 = pd.read_excel("assets/boxscore_partidos.xlsx")

df_1['Fecha'] = pd.to_datetime(df_1['Fecha'], format='%d/%m/%Y', errors='coerce')
df_1 = df_1.sort_values(by='Fecha', ascending=True)

def get_first_player(team):
    players = df[df['Team'] == team]['Jugadores']
    return players.iloc[0] if not players.empty else None

layout = dbc.Container([
    html.H1("Resumen de jugadores por equipos", className='text-center my-4'),

    dbc.Row([
        dbc.Col([
            html.Label("Selecciona un equipo", className='form-label'),
            dcc.Dropdown(
                id='dropdown-team',
                options=[{'label': equipo, 'value': equipo} for equipo in sorted(df['Team'].unique())],
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

        dbc.Col(html.Img(id='team-logo', style={'width': '100%', 'max-height': '150px', 'object-fit': 'contain'}), width=3),
        dbc.Col(html.Img(id='jugador-foto', style={'width': '100%', 'max-height': '150px', 'object-fit': 'contain'}), width=3),
    ]),

    dbc.Row([
        dbc.Col(dbc.Card(id='points-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
        dbc.Col(dbc.Card(id='rebound-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
        dbc.Col(dbc.Card(id='assists-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
        dbc.Col(dbc.Card(id='min-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
    ], class_name="my-4 g-3"),

    html.Div([
        html.H4("Gráficos de rendimientos por partido", className='text-center my-4'),
        dcc.DatePickerRange(
            id='selector_fecha',
            display_format='DD/MM/YYYY',
            start_date=df_1['Fecha'].min(),
            end_date=df_1['Fecha'].max(),
            className='custom-date-picker'
        ),
        dcc.Graph(id='graph_line')
    ])
], fluid=True)

@callback(
    [Output('dropdown-player', 'options'),
     Output('dropdown-player', 'value')],
    Input('dropdown-team', 'value')
)
def update_players_dropdown(selected_team):
    if selected_team:
        players = df[df['Team'] == selected_team]['Jugadores']
        options = [{'label': jugador, 'value': jugador} for jugador in players]
        first_player = get_first_player(selected_team)
        return options, first_player
    return [], None

@callback(
    [Output('selector_fecha', 'start_date'), Output('selector_fecha', 'end_date')],
    Input('dropdown-player', 'value')
)
def reset_date_range(selected_player):
    return df_1['Fecha'].min(), df_1['Fecha'].max()

@callback(
    Output('graph_line', 'figure'),
    [Input('selector_fecha', 'start_date'), Input('selector_fecha', 'end_date'), Input('dropdown-player', 'value')]
)
def actualizar_graph(fecha_min, fecha_max, selected_player):
    filtered_df = df_1[(df_1['Fecha'] >= fecha_min) & (df_1['Fecha'] <= fecha_max)]
    if not selected_player:
        return px.scatter(title="Selecciona un jugador para ver el gráfico")
    player_data = filtered_df[filtered_df['Jugadores'] == selected_player]
    player_data = player_data.sort_values(by='Fecha').reset_index(drop=True)
    player_data['ID'] = range(1, len(player_data) + 1)

    promedio_puntos = player_data['PTS'].mean()
    player_data['hover_text'] = 'Fecha: ' + player_data['Fecha'].dt.strftime('%d-%m-%Y') + '<br>' + 'Condición: ' + player_data['Condición'] + '<br>' + 'Puntos: ' + player_data['PTS'].astype(str)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=player_data['ID'], y=player_data['PTS'], mode='lines', line=dict(color='blue', width=1), name='Conexión', opacity=0.5, hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=player_data['ID'], y=[promedio_puntos] * len(player_data), mode='lines', line=dict(dash='dash', color='white'), name=f"Promedio: {promedio_puntos:.2f}", opacity=0.5, hoverinfo='skip'))

    for resultado, color in {'Gano': 'green', 'Perdio': 'red'}.items():
        subset = player_data[player_data['Resultado'] == resultado]
        fig.add_trace(go.Scatter(x=subset['ID'], y=subset['PTS'], mode='markers', marker=dict(color=color, size=12), text=subset['hover_text'], hoverinfo='text', name=resultado, visible=True))

    fig.update_layout(
        xaxis=dict(title="Partido (ID)", visible=False),
        yaxis=dict(title="Puntos", range=[0, player_data['PTS'].max() + 10]),
        template='plotly_dark',
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
    )
    return fig

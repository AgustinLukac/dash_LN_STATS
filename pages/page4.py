from dash import html, dcc, Input, Output, Dash, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path
import plotly.express as px  # Importar Plotly Express
from pathlib import Path


df = pd.read_excel("assets/Acumulados.xlsx")
df_1 = pd.read_excel("assets/boxscore_partidos.xlsx")

df_1['Fecha'] = pd.to_datetime(df_1['Fecha'], format='%d/%m/%Y', errors='coerce')
df_1 = df_1.sort_values(by='Fecha', ascending=True)



layout = dbc.Container([

    html.Header(
    dbc.Navbar(
        dbc.Container([
            # Logo y título
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg", height="40px")),
                    dbc.Col(dbc.NavbarBrand("Mi Dashboard", className="ms-2", style={"font-size": "24px", "color": "white"})),
                ], align="center", className="g-0"),
                href="#",
                style={"textDecoration": "none"},
            ),

             # Botón Toggler para menú en móviles
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),

            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("🏠 Inicio", href="#", className="text-white")),
                    dbc.NavItem(dbc.NavLink("📊 Reportes", href="#", className="text-white")),
                    dbc.NavItem(dbc.NavLink("📈 Análisis", href="#", className="text-white")),
                    dbc.NavItem(dbc.NavLink("⚙️ Configuración", href="#", className="text-white")),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                is_open=False,  # Inicialmente cerrado en móviles
                navbar=True
            ),

            # Ícono de usuario (opcional)
            html.A(
                html.Img(src="https://cdn-icons-png.flaticon.com/512/847/847969.png", height="30px"),
                href="#",
            )
        ], fluid=True),
        color="dark",
        dark=True
    ),
    style={"position": "fixed", "width": "100%", "zIndex": "1000", "top": "0px"}  # Fija el header arriba
),



 
    html.H1("Resumen de jugadores por equipos", className='text-center my-4', style={"paddingTop": "80px"}),

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
        ], width=3),

        # Columna para la foto del jugador
        dbc.Col([
            html.Div(
                html.Img(
                    id='jugador-foto',
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
        ], width=3),


    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.P("Selecciona un equipo y un jugador para ver los datos",
                        className="card-text text-center")
                ]),
                id='points-card',
                body=True,
                className="dashboard-card"
            ), xs=12, sm=6, md=3 
        ),
        dbc.Col(
            dbc.Card(
                id='rebound-card',
                body=True,
                className="dashboard-card"
            ), xs=12, sm=6, md=3 
        ),
        dbc.Col(
            dbc.Card(
                id='assists-card',
                body=True,
                className="dashboard-card"
            ), xs=12, sm=6, md=3 
        ),
        dbc.Col(
            dbc.Card(
                id='min-card',
                body=True,
                className="dashboard-card"
            ), xs=12, sm=6, md=3 
        ),
    ], class_name="my-4 g-3"),

    html.Div([
    html.H4("Gráficos de rendimientos por partido", className='text-center my-4'),

    html.Div(
        [
            html.Label(
                "Selecciona el rango de fechas:         ",
                style={
                    'font-size': '18px', 
                    'font-weight': 'bold',
                    'margin-bottom': '10px',
                    
                    }
                ),
            dcc.DatePickerRange(
                id='selector_fecha',
                start_date=df_1['Fecha'].min(),
                end_date=df_1['Fecha'].max(),
                display_format='DD/MM/YYYY',  # Formato de fecha dd/mm/yyyy
                start_date_placeholder_text='Inicio',
                end_date_placeholder_text='Fin',
                className='custom-date-picker',
                style={
                    'border': '1px solid #ccc',
                    'border-radius': '5px',
                    'padding': '5px',
                    'font-weight': 'bold',
                    'margin-left': '10px',
                    
                }
            )
        ],
        style={
            'margin-bottom': '20px',
            'padding': '10px',
            'border': '1px solid #ccc',
            'border-radius': '5px',
            'background-color': '#f9f9f9',
            'box-shadow': '0px 2px 5px rgba(0, 0, 0, 0.1)'
        }
    ),

    dcc.Graph(id='graph_line')
    ])

], fluid=True)

##### CALLBACKS #####

def get_first_player(team):
    players = df[df['Team'] == team].sort_values(by='MIN', ascending=False)
    return players.iloc[0]['Jugadores'] if not players.empty else None

# Actualizar Dropdown de jugadores
@callback(
    [Output('dropdown-player', 'options'),
     Output('dropdown-player', 'value')],
    Input('dropdown-team', 'value')
)
def update_players_dropdown(selected_team):
    if selected_team:
        players = df[df['Team'] == selected_team]['Jugadores'].sort_values()
        options = [{'label': jugador, 'value': jugador} for jugador in players]
        first_player = get_first_player(selected_team)
        return options, first_player
    return [], None

# Actualizar métricas del jugador
@callback(
    [ Output('points-card', 'children'),
     Output('rebound-card', 'children'),
     Output('assists-card', 'children'),
     Output('min-card', 'children'),
    ],
    Input('dropdown-player', 'value')
)
def update_player_info(selected_player):
    if selected_player:
        metricas = df[df['Jugadores'] == selected_player].iloc[0]

        perdidos_count = df_1[(df_1['Jugadores'] == selected_player) & (df_1['Resultado'] == 'Perdio')].shape[0]
        gano_count = df_1[(df_1['Jugadores'] == selected_player) & (df_1['Resultado'] == 'Gano')].shape[0]
        points = metricas['PTS']
        rebounds = metricas['RT']
        rebounds_def = metricas['DEF REB']
        rebounds_def_p = metricas['RD%']
        rebounds_of = metricas['OFF REB']
        rebounds_of_p = metricas['RO%']
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
        ppp = metricas['PPP']
        efg = metricas['EFG %']
        ts = metricas['TS %']
        pj = metricas['PJ']
        rtl = metricas['RTL %']

        return (

            dbc.CardBody([
                html.H2("ANOTACIÓN", className="card-title", **{"data-text": "ANOTACIÓN"}),
                html.Div([
                    html.H3(f"{points}", className="stat-value"),
                    html.P("Puntos", className="stat-label")
                ], className="text-center mb-4"),
                html.Div([
                    html.H4(f"{fgm_3} / {fga_3} - {fga_3_p * 100:.1f}%",
                        className="stat-value"),
                    html.P("Tiros de 3", className="stat-label")
                ], className="text-center mb-3"),
                html.Div([
                    html.H4(f"{fgm_2} / {fga_2} - {fga_2_p * 100:.1f}%",
                        className="stat-value"),
                    html.P("Tiros de 2", className="stat-label")
                ], className="text-center mb-3"),
                html.Div([
                    html.H4(f"{ftm} / {fta} - {fta_p * 100:.1f}%",
                        className="stat-value"),
                    html.P("Tiros de 1", className="stat-label")
                ], className="text-center mb-3"),
            ]),

            dbc.CardBody([
                html.H2("POSESIÓN", className="card-title", **{"data-text": "POSESIÓN"}),
                html.Div([
                    html.H3(f"{min}", className="stat-value"),
                    html.P("Minutos", className="stat-label")
                ], className="text-center mb-4"),
                html.Div([
                    html.H4(f"{usg* 100:.1f} % - {plays}",
                        className="stat-value"),
                    html.P("USG % - PLAYS", className="stat-label")
                ], className="text-center mb-3"),
                html.Div([
                    html.H4(f"{assists} - {assists_p * 100:.1f}%",
                        className="stat-value"),
                    html.P("AST - AST %", className="stat-label")
                ], className="text-center mb-3"),
                html.Div([
                    html.H4(f"{to} - {to_p*100:.1f} %",
                        className="stat-value"),
                    html.P("TO - TO %", className="stat-label")
                ], className="text-center mb-3"),
            ]),

            dbc.CardBody([
                html.H2("REBOTES", className="card-title", **{"data-text": "REBOTES"}),
                html.Div([
                    html.H3(f"{rebounds}", className="stat-value"),
                    html.P("RT", className="stat-label")
                ], className="text-center mb-4"),
                html.Div([
                    html.H4(f"{rebounds_of} - {rebounds_of_p * 100:.1f} %",
                        className="stat-value"),
                    html.P("RO - RO %", className="stat-label")
                ], className="text-center mb-3"),
                html.Div([
                    html.H4(f"{rebounds_def} - {rebounds_def_p * 100:.1f} %",
                        className="stat-value"),
                    html.P("RD - RD %", className="stat-label")
                ], className="text-center mb-3"),
                html.Div([
                    html.H4(f" {rtl *100:.1f} %",
                        className="stat-value"),
                    html.P("RTL %", className="stat-label")
                ], className="text-center mb-3"),
            ]),

            dbc.CardBody([
                html.H2("Performance", className="card-title", **{"data-text": "Performance"}),

                html.Div([
                    html.H4([
                        f"{pj} - (",
                        html.Span(f"{gano_count}", style={"color": "green"}),  # Verde
                        " - ",
                        html.Span(f"{perdidos_count}", style={"color": "red"}),  # Rojo
                        ")"
                    ], className="stat-value"),
                    html.P("PJ", className="stat-label")
                ], className="text-center mb-3"),

                html.Div([
                    html.H4(f"{ppp}",
                        className="stat-value"),
                    html.P("PPP", className="stat-label")
                ], className="text-center mb-3"),

                html.Div([
                    html.H4(f"{efg * 100:.1f} %",
                        className="stat-value"),
                    html.P("EFG %", className="stat-label")
                ], className="text-center mb-3"),

                html.Div([
                    html.H4(f"{ts * 100:.1f} %",
                        className="stat-value"),
                    html.P("TS %", className="stat-label")
                ], className="text-center mb-3"),


             ])
            
            
        )
    return (

        dbc.CardBody([
            html.H3("N/A", className="stat-value"),
            html.P("Anotación", className="stat-label")
        ]),

        dbc.CardBody([
            html.H3("N/A", className="stat-value"),
            html.P("Posesión", className="stat-label")
        ]),

        dbc.CardBody([
            html.H3("N/A", className="stat-value"),
            html.P("Minutos", className="stat-label")
        ]),

        dbc.CardBody([
            html.H3("N/A", className="stat-value"),
            html.P("Performance", className="stat-label")
        ])
        
    )
##################################################################################################
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

# Actualizar foto del jugador
@callback(
    Output('jugador-foto', 'src'),
    Input('dropdown-player', 'value')
)
def update_team_logo(selected_player):
    if selected_player:
        # Filtrar el DataFrame por el jugador seleccionado
        jugador_info = df[df['Jugadores'] == selected_player]
        
        # Verificar si existe un resultado y obtener la ruta de la imagen
        if not jugador_info.empty:
            ruta_imagen = jugador_info.iloc[0]['Imagen']  # Obtener el valor de la columna 'Imagen'
            return f"/assets/Player_fotos/{ruta_imagen}.png"  # Construir la ruta completa
    
    # Retornar imagen por defecto si no hay jugador seleccionado o no se encuentra
    return "/assets/logos/default.png"

@callback(Output('graph_line', 'figure'),
          [Input('selector_fecha', 'start_date'),
           Input('selector_fecha', 'end_date'),
           Input('dropdown-player', 'value')])
def actualizar_graph(fecha_min, fecha_max, selected_player):
    # Filtrar el DataFrame por las fechas seleccionadas
    filtered_df = df_1[(df_1['Fecha'] >= fecha_min) & (df_1['Fecha'] <= fecha_max)]

    if not selected_player:
        return px.scatter(title="Selecciona un jugador para ver el gráfico")

    # Filtrar por el jugador seleccionado
    player_data = filtered_df[filtered_df['Jugadores'] == selected_player]

    # Ordenar por fecha y asignar IDs secuenciales
    player_data = player_data.sort_values(by='Fecha').reset_index(drop=True)
    player_data['ID'] = range(1, len(player_data) + 1)

    promedio_puntos = player_data['PTS'].mean()

    # Crear una columna de texto personalizada para las tooltips
    player_data['hover_text'] = (
        'Fecha: ' + player_data['Fecha'].dt.strftime('%d-%m-%Y') + '<br>' +
        'Condición: ' + player_data['Condición'] + '<br>' +
        'Puntos: ' + player_data['PTS'].astype(str)
    )



    # Crear el gráfico en Plotly
    fig = go.Figure()

    # Agregar la línea azul primero
    fig.add_trace(go.Scatter(
        x=player_data['ID'],
        y=player_data['PTS'],
        mode='lines',
        line=dict(color='blue', width=1),
        name='Conexión',
        opacity=0.5,
        hoverinfo='skip'
    ))

    # Agregar una línea de promedio
    fig.add_trace(go.Scatter(
        x=player_data['ID'],
        y=[promedio_puntos] * len(player_data),
        mode='lines',
        line=dict(dash='dash', color='white'),
        name=f"Promedio: {promedio_puntos:.2f}",
        opacity=0.5,
        hoverinfo='skip'
    ))

    # Agregar los puntos rojos y verdes según el resultado
    colores = {'Gano': 'green', 'Perdio': 'red'}
    for resultado, color in colores.items():
        subset = player_data[player_data['Resultado'] == resultado]
        fig.add_trace(go.Scatter(
            x=subset['ID'],
            y=subset['PTS'],
            mode='markers',
            marker=dict(color=color, size=12),
            text=subset['hover_text'],  # Texto personalizado para tooltips
            hoverinfo='text',  # Mostrar solo el texto personalizado
            name=resultado
        ))

        # Agregar texto con los puntos 2.5 unidades abajo del punto
    for _, row in player_data.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['ID']],
            y=[row['PTS'] - 1.5],  # Colocar 2.5 unidades abajo del punto
            mode='text',
            text=[f"{row['PTS']}"],  # Texto con los puntos
            textfont=dict(color="white", size=14),  # Formato del texto
            showlegend=False,
            hoverinfo='skip'
        ))

    # Agregar los logos como imágenes
    for _, row in player_data.iterrows():
        logo_path = f"assets/logos/{row['Opp']}.png"
        if Path(logo_path).exists():
            fig.add_layout_image(
                source=f"/{logo_path}",
                x=row['ID'],
                y=row['PTS'] + 2.5,
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                sizex=3,
                sizey=3,
                opacity=1
            )

    # Ajustar el rango de los ejes y otros detalles
    fig.update_layout(
        xaxis=dict(title="Partido (ID)",
                visible=False,  # Ocultar el eje X 
                automargin=True,
                showgrid=False,
                zeroline=False),
        yaxis=dict(title="Puntos", 
                range=[-5, player_data['PTS'].max() + 10],
                tickvals=[i for i in range(0, player_data['PTS'].max() + 11, 5)],  # Escala visible desde 0
                ticktext=[str(i) for i in range(0, player_data['PTS'].max() + 11, 5)],  # Etiquetas visibles desde 0
                zeroline=False),
        margin=dict(l=20, r=20, t=40, b=10),
        template='plotly_dark',

        # 🔹 Mueve la leyenda abajo del gráfico en móviles
        legend=dict(
            orientation="h",  # Leyenda horizontal
            yanchor="top",  # Anclar arriba
            y=-0.2,  # Ajustar para que quede fuera del gráfico
            xanchor="center",  # Centrar
            x=0.5
        )
    )

    return fig


@callback(
    [Output('selector_fecha', 'start_date'), Output('selector_fecha', 'end_date')],
    Input('dropdown-player', 'value')
)
def reset_date_range(selected_player):
    return df_1['Fecha'].min(), df_1['Fecha'].max()
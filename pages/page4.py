from dash import html, dcc, Input, Output, Dash, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path
import plotly.express as px  # Importar Plotly Express
from pathlib import Path
import numpy as np


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
                    dbc.Col(dbc.NavbarBrand("Dashboard | AI - STATS", className="ms-2", style={"font-size": "24px", "color": "white"})),
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

    dbc.Row([
        dbc.Col([
            html.Label("Selecciona un equipo", 
                    className='form-label',
                    style={'color': 'white'}),
            dcc.Dropdown(
                id='dropdown-team',
                options=[
                    {'label': equipo, 'value': equipo}
                    for equipo in sorted(df['Team'].unique())
                ],
                placeholder="Selecciona un equipo",
                className="mb-3",
                clearable=True,
                searchable=True,
                style={
                    'backgroundColor': '#1e1e1e',
                    'color': 'white'
                }
            ),
            html.Label("Selecciona un jugador", 
                    className='form-label',
                    style={'color': 'white'}),
            dcc.Dropdown(
                id='dropdown-player',
                placeholder="Selecciona un jugador",
                className="mb-3",
                clearable=True,
                searchable=True,
                style={
                    'backgroundColor': '#1e1e1e',
                    'color': 'white'
                }
            ),
            html.Label("Seleccionar Condición", 
                    className='form-label',
                    style={'color': 'white'}),
            dcc.Dropdown(
                id='dropdown-condition',
                placeholder="Seleccionar Condición",
                className="mb-3",
                clearable=True,
                searchable=True,
                style={
                    'backgroundColor': '#1e1e1e',
                    'color': 'white'
                }
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

# Actualizar Dropdown de Condcion
@callback(
    [Output('dropdown-condition', 'options'),
     Output('dropdown-condition', 'value')],
    Input('dropdown-player', 'value')
)
def update_condition_dropdown(selected_condition):
    if selected_condition:
        # Filtramos df_1 para obtener las condiciones del jugador seleccionado
        condiciones = df_1[df_1['Jugadores'] == selected_condition]['Condición'].unique()
        
        # Convertimos a lista y ordenamos
        condiciones = sorted(condiciones)

        # Agregamos la opción "Todos" manualmente
        condiciones.insert(0, "Todos")

        # Creamos la lista de opciones para el Dropdown
        options = [{'label': condicion, 'value': condicion} for condicion in condiciones]

        # Seleccionamos "Todos" como valor por defecto
        return options, "Todos"

    return [], None  # Si no hay jugador seleccionado, vaciamos el dropdown



# Actualizar métricas del jugador
@callback(
    [ Output('points-card', 'children'),
     Output('rebound-card', 'children'),
     Output('assists-card', 'children'),
     Output('min-card', 'children'),
    ],
    Input('dropdown-player', 'value'),
    Input('dropdown-team', 'value'),
    Input('dropdown-condition', 'value')

)
def update_player_info(selected_player,selected_team,selected_condition):
        
    # # Si la condición es "Todos", se usa df
    # if selected_condition == "Todos":
    #     metricas = df[(df['Jugadores'] == selected_player) & (df['Team'] == selected_team)]

    # else:
    #     metricas = df_1[(df_1['Jugadores'] == selected_player) & 
    #                      (df_1['Condición'] == selected_condition) & 
    #                      (df_1['Team'] == selected_team)]
        
    #     # Hacemos un groupby para calcular los promedios de las métricas
    #     metricas = metricas.groupby(['Jugadores', 'Team']).mean(numeric_only=True).reset_index()
    if selected_player:
        metricas = df[(df['Jugadores'] == selected_player)&(df['Team'] == selected_team)].iloc[0]
        

        perdidos_count = df_1[(df_1['Team'] == selected_team)&(df_1['Jugadores'] == selected_player) & (df_1['Resultado'] == 'Perdio')].shape[0]
        gano_count = df_1[(df_1['Team'] == selected_team)&(df_1['Jugadores'] == selected_player) & (df_1['Resultado'] == 'Gano')].shape[0]
        
        
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
                        f"{pj} ",
                        html.Span([
                            " (",
                            html.Span(f"{gano_count}", style={"color": "green", "opacity": "0.85"}),
                            " - ",
                            html.Span(f"{perdidos_count}", style={"color": "red", "opacity": "0.85"}),
                            ")"
                        ], style={"font-size": "0.7em", "opacity": "0.7"})
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
            html.H3("- -", className="stat-value"),
            html.P("Anotación", className="stat-label")
        ]),

        dbc.CardBody([
            html.H3("- -", className="stat-value"),
            html.P("Posesión", className="stat-label")
        ]),

        dbc.CardBody([
            html.H3("- -", className="stat-value"),
            html.P("Minutos", className="stat-label")
        ]),

        dbc.CardBody([
            html.H3("- -", className="stat-value"),
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
           Input('dropdown-player', 'value'),
           Input('dropdown-team', 'value')])

def actualizar_graph(fecha_min, fecha_max, selected_player, selected_team):

    # Filtrar por fechas
    filtered_df = df_1[(df_1['Fecha'] >= fecha_min) & (df_1['Fecha'] <= fecha_max)]

    # Pantalla vacía si no hay jugador
    if not selected_player:
        fig = px.scatter(template="plotly_white")
        fig.update_layout(
            title=dict(
                text="📊 Selecciona un jugador para visualizar sus estadísticas 📈",
                x=0.5, y=0.5,
                xanchor="center", yanchor="middle",
                font=dict(size=20, color="#6B7280", family="Arial, sans-serif"),
            ),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=100, b=100),
        )
        fig.add_shape(
            type="rect",
            x0=0.2, y0=0.2, x1=0.8, y1=0.8,
            line=dict(color="#E5E7EB", width=2),
            fillcolor="rgba(243, 244, 246, 0.5)",
            layer="below",
        )
        return fig

    # Filtrar por jugador y team
    player_data = filtered_df[
        (filtered_df["Jugadores"] == selected_player) &
        (filtered_df["Team"] == selected_team)
    ].copy()

    # Ordenar por fecha y ID secuencial
    player_data = player_data.sort_values(by="Fecha").reset_index(drop=True)
    player_data["ID"] = np.arange(1, len(player_data) + 1)

    # ---- Normalización 3FG % a 0..1 ----
    # Si viene como 0..100, lo pasamos a 0..1
    y = pd.to_numeric(player_data["3FG %"], errors="coerce")
    if y.dropna().max() is not None and y.dropna().max() > 1.5:
        y = y / 100.0
    player_data["3FG_pct_01"] = y.fillna(0).clip(0, 1)

    promedio = float(player_data["3FG_pct_01"].mean())

    # Tooltip
    player_data["hover_text"] = (
        "Fecha: " + player_data["Fecha"].dt.strftime("%d-%m-%Y") + "<br>" +
        "Condición: " + player_data["Condición"].astype(str) + "<br>" +
        "Puntos: " + player_data["PTS"].astype(str) + "<br>" +
        "3FG%: " + (player_data["3FG_pct_01"] * 100).round(1).astype(str) + " %"
    )

    fig = go.Figure()

    # Línea conexión
    fig.add_trace(go.Scatter(
        x=player_data["ID"],
        y=player_data["3FG_pct_01"],
        mode="lines",
        line=dict(color="blue", width=1),
        name="Conexión",
        opacity=0.5,
        hoverinfo="skip",
    ))

    # Línea promedio
    fig.add_trace(go.Scatter(
        x=player_data["ID"],
        y=[promedio] * len(player_data),
        mode="lines",
        line=dict(dash="dash", color="white"),
        name=f"Promedio: {promedio*100:.1f} %",
        opacity=0.5,
        hoverinfo="skip",
    ))

    # Puntos por resultado
    colores = {"Gano": "green", "Perdio": "red"}
    for resultado, color in colores.items():
        subset = player_data[player_data["Resultado"] == resultado]
        fig.add_trace(go.Scatter(
            x=subset["ID"],
            y=subset["3FG_pct_01"],
            mode="markers",
            marker=dict(color=color, size=12),
            text=subset["hover_text"],
            hoverinfo="text",
            name=resultado,
        ))

    # Labels debajo de cada punto: "15.3 %"
    for _, r in player_data.iterrows():
        fig.add_trace(go.Scatter(
            x=[r["ID"]],
            y=[max(r["3FG_pct_01"] - 0.06, -0.02)],  # offset hacia abajo con límite
            mode="text",
            text=[f"{r['3FG_pct_01']*100:.1f} %"],
            textfont=dict(color="white", size=14),
            showlegend=False,
            hoverinfo="skip",
        ))

    # Logos (si existe columna Opp)
    if "Opp" in player_data.columns:
        for _, r in player_data.iterrows():
            logo_path = f"assets/logos/{r['Opp']}.png"
            if Path(logo_path).exists():
                fig.add_layout_image(
                    source=f"/{logo_path}",
                    x=r["ID"],
                    y=min(r["3FG_pct_01"] + 0.08, 1.02),
                    xref="x",
                    yref="y",
                    xanchor="center",
                    yanchor="middle",
                    sizex=0.25,
                    sizey=0.25,
                    opacity=1,
                )

    # ---- EJE Y 0..1 pero mostrado como % con espacio ----
    tickvals = np.linspace(0, 1, 6)  # 0.0, 0.2, ..., 1.0
    ticktext = [f"{v*100:.1f} %" for v in tickvals]  # "100.0 %"

    fig.update_layout(
        xaxis=dict(
            title="Partido (ID)",
            visible=False,
            automargin=True,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            title="3FG %",
            range=[-0.05, 1.05],          # márgenes para ver 0% y 100% cómodos
            tickvals=tickvals,
            ticktext=ticktext,
            showgrid=True,
            zeroline=False,
        ),
        margin=dict(l=40, r=20, t=40, b=10),
        template="plotly_dark",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig



# #     return None
# from dash import html, dcc, Input, Output, Dash, callback
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objs as go
# from pathlib import Path
# import plotly.express as px
# import numpy as np

# # =========================
# # DATA
# # =========================
# df = pd.read_excel("assets/Acumulados.xlsx")               # acumulados por jugador/equipo
# df_1 = pd.read_excel("assets/boxscore_partidos.xlsx")      # boxscore por partido

# df_1['Fecha'] = pd.to_datetime(df_1['Fecha'], format='%d/%m/%Y', errors='coerce')
# df_1 = df_1.sort_values(by='Fecha', ascending=True)

# # =========================
# # APP (si lo usás como page, podés ignorar esto)
# # =========================
# # app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# # app.layout = layout

# # =========================
# # HELPERS
# # =========================
# def get_first_player(team):
#     players = df[df['Team'] == team].sort_values(by='MIN', ascending=False)
#     return players.iloc[0]['Jugadores'] if not players.empty else None

# def safe_pct_to_01(series: pd.Series) -> pd.Series:
#     """Convierte porcentaje a escala 0..1 si viene 0..100."""
#     y = pd.to_numeric(series, errors="coerce")
#     mx = y.dropna().max() if not y.dropna().empty else None
#     if mx is not None and mx > 1.5:
#         y = y / 100.0
#     return y.clip(0, 1)

# def apply_filters_boxscore(
#     base_df: pd.DataFrame,
#     team: str | None,
#     player: str | None,
#     condition: str | None,
#     result: str | None,
#     last_n: str | None,
#     date_min=None,
#     date_max=None,
# ) -> pd.DataFrame:
#     """Filtra df_1 (boxscore_partidos) por equipo, jugador, condición, resultado, fechas y últimos N."""
#     d = base_df.copy()

#     if team:
#         d = d[d["Team"] == team]
#     if player:
#         d = d[d["Jugadores"] == player]

#     # Fecha range (si llega)
#     if date_min is not None and date_max is not None:
#         d = d[(d["Fecha"] >= date_min) & (d["Fecha"] <= date_max)]

#     # Condición
#     if condition and condition != "Todos":
#         d = d[d["Condición"] == condition]

#     # Resultado
#     if result and result != "Todos":
#         d = d[d["Resultado"] == result]

#     # Últimos N (después de filtrar lo anterior)
#     if last_n in ("Ultimos 5", "Ultimos 3"):
#         n = 5 if last_n == "Ultimos 5" else 3
#         d = d.sort_values("Fecha", ascending=True)
#         d = d.tail(n)

#     return d

# def should_use_acumulados(condition: str | None, result: str | None, last_n: str | None) -> bool:
#     """
#     Tarjetas:
#     - Usar df (Acumulados) SOLO cuando: condition=Todos AND result=Todos AND last_n=Todos
#     - En cualquier otro caso, usar df_1 filtrado.
#     """
#     return (condition in (None, "Todos")) and (result in (None, "Todos")) and (last_n in (None, "Todos"))

# def empty_fig_message():
#     fig = px.scatter(template="plotly_white")
#     fig.update_layout(
#         title=dict(
#             text="📊 Selecciona un jugador para visualizar sus estadísticas 📈",
#             x=0.5, y=0.5,
#             xanchor="center", yanchor="middle",
#             font=dict(size=20, color="#6B7280", family="Arial, sans-serif"),
#         ),
#         xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
#         yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
#         showlegend=False,
#         plot_bgcolor="white",
#         paper_bgcolor="white",
#         margin=dict(t=100, b=100),
#     )
#     fig.add_shape(
#         type="rect",
#         x0=0.2, y0=0.2, x1=0.8, y1=0.8,
#         line=dict(color="#E5E7EB", width=2),
#         fillcolor="rgba(243, 244, 246, 0.5)",
#         layer="below",
#     )
#     return fig

# # =========================
# # LAYOUT
# # =========================
# layout = dbc.Container([

#     html.Header(
#         dbc.Navbar(
#             dbc.Container([
#                 html.A(
#                     dbc.Row([
#                         dbc.Col(html.Img(src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg", height="40px")),
#                         dbc.Col(dbc.NavbarBrand("Dashboard | AI - STATS", className="ms-2",
#                                                style={"font-size": "24px", "color": "white"})),
#                     ], align="center", className="g-0"),
#                     href="#",
#                     style={"textDecoration": "none"},
#                 ),
#                 dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
#                 dbc.Collapse(
#                     dbc.Nav([
#                         dbc.NavItem(dbc.NavLink("🏠 Inicio", href="#", className="text-white")),
#                         dbc.NavItem(dbc.NavLink("📊 Reportes", href="#", className="text-white")),
#                         dbc.NavItem(dbc.NavLink("📈 Análisis", href="#", className="text-white")),
#                         dbc.NavItem(dbc.NavLink("⚙️ Configuración", href="#", className="text-white")),
#                     ], className="ms-auto", navbar=True),
#                     id="navbar-collapse",
#                     is_open=False,
#                     navbar=True
#                 ),
#                 html.A(html.Img(src="https://cdn-icons-png.flaticon.com/512/847/847969.png", height="30px"), href="#"),
#             ], fluid=True),
#             color="dark",
#             dark=True
#         ),
#         style={"position": "fixed", "width": "100%", "zIndex": "1000", "top": "0px"}
#     ),

#     html.H1("Resumen de jugadores por equipos", className='text-center my-4', style={"paddingTop": "80px"}),

#     dbc.Row([
#         dbc.Col([

#             html.Label("Selecciona un equipo", className='form-label', style={'color': 'white'}),
#             dcc.Dropdown(
#                 id='dropdown-team',
#                 options=[{'label': equipo, 'value': equipo} for equipo in sorted(df['Team'].unique())],
#                 placeholder="Selecciona un equipo",
#                 className="mb-3",
#                 clearable=True,
#                 searchable=True,
#                 style={'backgroundColor': '#1e1e1e', 'color': 'white'}
#             ),

#             html.Label("Selecciona un jugador", className='form-label', style={'color': 'white'}),
#             dcc.Dropdown(
#                 id='dropdown-player',
#                 placeholder="Selecciona un jugador",
#                 className="mb-3",
#                 clearable=True,
#                 searchable=True,
#                 style={'backgroundColor': '#1e1e1e', 'color': 'white'}
#             ),

#             html.Label("Condición", className='form-label', style={'color': 'white'}),
#             dcc.Dropdown(
#                 id='dropdown-condition',
#                 placeholder="Condición",
#                 className="mb-3",
#                 clearable=False,
#                 searchable=False,
#                 style={'backgroundColor': '#1e1e1e', 'color': 'white'}
#             ),

#             html.Label("Resultado", className='form-label', style={'color': 'white'}),
#             dcc.Dropdown(
#                 id='dropdown-result',
#                 options=[
#                     {"label": "Todos", "value": "Todos"},
#                     {"label": "Gano", "value": "Gano"},
#                     {"label": "Perdio", "value": "Perdio"},
#                 ],
#                 value="Todos",
#                 placeholder="Resultado",
#                 className="mb-3",
#                 clearable=False,
#                 searchable=False,
#                 style={'backgroundColor': '#1e1e1e', 'color': 'white'}
#             ),

#             html.Label("Partidos", className='form-label', style={'color': 'white'}),
#             dcc.Dropdown(
#                 id='dropdown-lastn',
#                 options=[
#                     {"label": "Todos", "value": "Todos"},
#                     {"label": "Ultimos 5 partidos", "value": "Ultimos 5"},
#                     {"label": "Ultimos 3 partidos", "value": "Ultimos 3"},
#                 ],
#                 value="Todos",
#                 placeholder="Cantidad de partidos",
#                 className="mb-3",
#                 clearable=False,
#                 searchable=False,
#                 style={'backgroundColor': '#1e1e1e', 'color': 'white'}
#             ),

#             html.Label("Offense / Defense"),
#             dbc.Switch(
#                 id="offense-defense",
#                 value=True,
#                 className="custom-switch"
#             ),

#         ], width=6),

#         dbc.Col([
#             html.Div(
#                 html.Img(
#                     id='team-logo',
#                     style={'width': '100%', 'height': 'auto', 'max-height': '150px', 'object-fit': 'contain'}
#                 ),
#                 style={'padding': '10px', 'text-align': 'center', 'height': '100%'}
#             )
#         ], width=3),

#         dbc.Col([
#             html.Div(
#                 html.Img(
#                     id='jugador-foto',
#                     style={'width': '100%', 'height': 'auto', 'max-height': '250px', 'object-fit': 'contain'}
#                 ),
#                 style={'padding': '10px', 'text-align': 'center', 'height': '100%'}
#             )
#         ], width=3),

#     ]),

#     dbc.Row([
#         dbc.Col(dbc.Card(dbc.CardBody([html.P("Selecciona un equipo y un jugador para ver los datos", className="card-text text-center")]),
#                         id='points-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
#         dbc.Col(dbc.Card(id='rebound-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
#         dbc.Col(dbc.Card(id='assists-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
#         dbc.Col(dbc.Card(id='min-card', body=True, className="dashboard-card"), xs=12, sm=6, md=3),
#     ], class_name="my-4 g-3"),

#     html.Div([
#         html.H4("Gráficos de rendimientos por partido", className='text-center my-4'),

#         html.Div(
#             [
#                 html.Label(
#                     "Selecciona el rango de fechas:         ",
#                     style={'font-size': '18px', 'font-weight': 'bold', 'margin-bottom': '10px'}
#                 ),
#                 dcc.DatePickerRange(
#                     id='selector_fecha',
#                     start_date=df_1['Fecha'].min(),
#                     end_date=df_1['Fecha'].max(),
#                     display_format='DD/MM/YYYY',
#                     start_date_placeholder_text='Inicio',
#                     end_date_placeholder_text='Fin',
#                     className='custom-date-picker',
#                     style={
#                         'border': '1px solid #ccc',
#                         'border-radius': '5px',
#                         'padding': '5px',
#                         'font-weight': 'bold',
#                         'margin-left': '10px',
#                     }
#                 )
#             ],
#             style={
#                 'margin-bottom': '20px',
#                 'padding': '10px',
#                 'border': '1px solid #ccc',
#                 'border-radius': '5px',
#                 'background-color': '#f9f9f9',
#                 'box-shadow': '0px 2px 5px rgba(0, 0, 0, 0.1)'
#             }
#         ),

#         dcc.Graph(id='graph_line'),

#         html.Div(style={
#             'margin-bottom': '20px',
#             'padding': '10px',
#             'border': '1px solid #ccc',
#             'border-radius': '5px',
#             'background-color': '#f9f9f9',
#             'box-shadow': '0px 2px 5px rgba(0, 0, 0, 0.1)'
#         }),

#         dcc.Graph(id='graph_line11')

#     ]),

# ], fluid=True)

# # =========================
# # CALLBACKS
# # =========================

# @callback(
#     [Output('dropdown-player', 'options'),
#      Output('dropdown-player', 'value')],
#     Input('dropdown-team', 'value')
# )
# def update_players_dropdown(selected_team):
#     if selected_team:
#         players = df[df['Team'] == selected_team]['Jugadores'].sort_values()
#         options = [{'label': jugador, 'value': jugador} for jugador in players]
#         first_player = get_first_player(selected_team)
#         return options, first_player
#     return [], None

# @callback(
#     [Output('dropdown-condition', 'options'),
#      Output('dropdown-condition', 'value')],
#     Input('dropdown-player', 'value')
# )
# def update_condition_dropdown(selected_player):
#     if selected_player:
#         condiciones = df_1[df_1['Jugadores'] == selected_player]['Condición'].dropna().unique()
#         condiciones = sorted(list(condiciones))
#         condiciones.insert(0, "Todos")
#         options = [{'label': c, 'value': c} for c in condiciones]
#         return options, "Todos"
#     return [], None

# @callback(
#     [Output('points-card', 'children'),
#      Output('rebound-card', 'children'),
#      Output('assists-card', 'children'),
#      Output('min-card', 'children')],
#     [
#         Input('dropdown-player', 'value'),
#         Input('dropdown-team', 'value'),
#         Input('dropdown-condition', 'value'),
#         Input('dropdown-result', 'value'),
#         Input('dropdown-lastn', 'value'),
#     ]
# )
# def update_player_info(selected_player, selected_team, selected_condition, selected_result, selected_lastn):

#     if not selected_player or not selected_team:
#         return (
#             dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Anotación", className="stat-label")]),
#             dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Posesión", className="stat-label")]),
#             dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Rebotes", className="stat-label")]),
#             dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Performance", className="stat-label")]),
#         )

#     use_acc = should_use_acumulados(selected_condition, selected_result, selected_lastn)

#     # ==========
#     # TARJETAS: ACUMULADOS
#     # ==========
#     if use_acc:
#         row = df[(df['Jugadores'] == selected_player) & (df['Team'] == selected_team)]
#         if row.empty:
#             return (
#                 dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Anotación", className="stat-label")]),
#                 dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Posesión", className="stat-label")]),
#                 dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Rebotes", className="stat-label")]),
#                 dbc.CardBody([html.H3("- -", className="stat-value"), html.P("Performance", className="stat-label")]),
#             )

#         metricas = row.iloc[0]

#         # PJ / Ganó / Perdió desde df_1 (total, como venías)
#         perdidos_count = df_1[(df_1['Team'] == selected_team) & (df_1['Jugadores'] == selected_player) & (df_1['Resultado'] == 'Perdio')].shape[0]
#         gano_count = df_1[(df_1['Team'] == selected_team) & (df_1['Jugadores'] == selected_player) & (df_1['Resultado'] == 'Gano')].shape[0]

#     # ==========
#     # TARJETAS: BOX SCORE (FILTRADO)
#     # ==========
#     else:
#         d = apply_filters_boxscore(
#             df_1,
#             team=selected_team,
#             player=selected_player,
#             condition=selected_condition,
#             result=selected_result,
#             last_n=selected_lastn,
#             date_min=None,
#             date_max=None,
#         )

#         if d.empty:
#             return (
#                 dbc.CardBody([html.H3("Sin datos", className="stat-value"), html.P("Anotación", className="stat-label")]),
#                 dbc.CardBody([html.H3("Sin datos", className="stat-value"), html.P("Posesión", className="stat-label")]),
#                 dbc.CardBody([html.H3("Sin datos", className="stat-value"), html.P("Rebotes", className="stat-label")]),
#                 dbc.CardBody([html.H3("Sin datos", className="stat-value"), html.P("Performance", className="stat-label")]),
#             )

#         # Promedios por el subconjunto filtrado
#         metricas = d.mean(numeric_only=True)

#         gano_count = int((d["Resultado"] == "Gano").sum()) if "Resultado" in d.columns else 0
#         perdidos_count = int((d["Resultado"] == "Perdio").sum()) if "Resultado" in d.columns else 0

#         # Si en df_1 no existe PJ como columna promedio, lo calculamos:
#         metricas = metricas.copy()
#         metricas["PJ"] = len(d)

#     # =========================
#     # Extract metrics (mismo formato tuyo)
#     # =========================
#     points = metricas.get('PTS', np.nan)
#     rebounds = metricas.get('RT', np.nan)
#     rebounds_def = metricas.get('DEF REB', np.nan)
#     rebounds_def_p = metricas.get('RD%', metricas.get('RD %', np.nan))
#     rebounds_of = metricas.get('OFF REB', np.nan)
#     rebounds_of_p = metricas.get('RO%', metricas.get('RO %', np.nan))
#     assists = metricas.get('AST', np.nan)
#     assists_p = metricas.get('AST %', np.nan)
#     mins = metricas.get('MIN', np.nan)

#     fgm_3 = metricas.get('3FGM', np.nan)
#     fga_3 = metricas.get('3FGA', np.nan)
#     fga_3_p = metricas.get('3FG %', np.nan)

#     fga_2 = metricas.get('2FGA', np.nan)
#     fgm_2 = metricas.get('2FGM', np.nan)
#     fga_2_p = metricas.get('2FG %', np.nan)

#     fta = metricas.get('FTA', np.nan)
#     ftm = metricas.get('FTM', np.nan)
#     fta_p = metricas.get('FT %', np.nan)

#     to = metricas.get('TO', np.nan)
#     to_p = metricas.get('TO %', np.nan)
#     usg = metricas.get('USG %', np.nan)
#     plays = metricas.get('PLAYS', np.nan)
#     ppp = metricas.get('PPP', np.nan)
#     efg = metricas.get('EFG %', np.nan)
#     ts = metricas.get('TS %', np.nan)
#     pj = metricas.get('PJ', np.nan)
#     rtl = metricas.get('RTL %', np.nan)

#     def fmt_num(x, nd=1):
#         try:
#             if pd.isna(x):
#                 return "- -"
#             return f"{float(x):.{nd}f}"
#         except Exception:
#             return str(x)

#     def fmt_intish(x):
#         try:
#             if pd.isna(x):
#                 return "- -"
#             # si viene float tipo 12.0 -> 12
#             if float(x).is_integer():
#                 return str(int(float(x)))
#             return str(x)
#         except Exception:
#             return str(x)

#     def fmt_pct01(x):
#         # viene 0..1
#         try:
#             if pd.isna(x):
#                 return "- -"
#             return f"{float(x)*100:.1f}%"
#         except Exception:
#             return str(x)

#     return (
#         dbc.CardBody([
#             html.H2("ANOTACIÓN", className="card-title", **{"data-text": "ANOTACIÓN"}),
#             html.Div([
#                 html.H3(f"{fmt_num(points,0) if str(points)!='nan' else '- -'}", className="stat-value"),
#                 html.P("Puntos", className="stat-label")
#             ], className="text-center mb-4"),
#             html.Div([
#                 html.H4(f"{fmt_intish(fgm_3)} / {fmt_intish(fga_3)} - {fmt_pct01(fga_3_p)}",
#                         className="stat-value"),
#                 html.P("Tiros de 3", className="stat-label")
#             ], className="text-center mb-3"),
#             html.Div([
#                 html.H4(f"{fmt_intish(fgm_2)} / {fmt_intish(fga_2)} - {fmt_pct01(fga_2_p)}",
#                         className="stat-value"),
#                 html.P("Tiros de 2", className="stat-label")
#             ], className="text-center mb-3"),
#             html.Div([
#                 html.H4(f"{fmt_intish(ftm)} / {fmt_intish(fta)} - {fmt_pct01(fta_p)}",
#                         className="stat-value"),
#                 html.P("Tiros de 1", className="stat-label")
#             ], className="text-center mb-3"),
#         ]),

#         dbc.CardBody([
#             html.H2("POSESIÓN", className="card-title", **{"data-text": "POSESIÓN"}),
#             html.Div([
#                 html.H3(f"{fmt_num(mins,1)}", className="stat-value"),
#                 html.P("Minutos", className="stat-label")
#             ], className="text-center mb-4"),
#             html.Div([
#                 html.H4(f"{fmt_pct01(usg)} - {fmt_num(plays,0)}", className="stat-value"),
#                 html.P("USG % - PLAYS", className="stat-label")
#             ], className="text-center mb-3"),
#             html.Div([
#                 html.H4(f"{fmt_num(assists,1)} - {fmt_pct01(assists_p)}", className="stat-value"),
#                 html.P("AST - AST %", className="stat-label")
#             ], className="text-center mb-3"),
#             html.Div([
#                 html.H4(f"{fmt_num(to,1)} - {fmt_pct01(to_p)}", className="stat-value"),
#                 html.P("TO - TO %", className="stat-label")
#             ], className="text-center mb-3"),
#         ]),

#         dbc.CardBody([
#             html.H2("REBOTES", className="card-title", **{"data-text": "REBOTES"}),
#             html.Div([
#                 html.H3(f"{fmt_num(rebounds,1)}", className="stat-value"),
#                 html.P("RT", className="stat-label")
#             ], className="text-center mb-4"),
#             html.Div([
#                 html.H4(f"{fmt_num(rebounds_of,1)} - {fmt_pct01(rebounds_of_p)}", className="stat-value"),
#                 html.P("RO - RO %", className="stat-label")
#             ], className="text-center mb-3"),
#             html.Div([
#                 html.H4(f"{fmt_num(rebounds_def,1)} - {fmt_pct01(rebounds_def_p)}", className="stat-value"),
#                 html.P("RD - RD %", className="stat-label")
#             ], className="text-center mb-3"),
#             html.Div([
#                 html.H4(f"{fmt_pct01(rtl)}", className="stat-value"),
#                 html.P("RTL %", className="stat-label")
#             ], className="text-center mb-3"),
#         ]),

#         dbc.CardBody([
#             html.H2("Performance", className="card-title", **{"data-text": "Performance"}),

#             html.Div([
#                 html.H4([
#                     f"{fmt_intish(pj)} ",
#                     html.Span([
#                         " (",
#                         html.Span(f"{gano_count}", style={"color": "green", "opacity": "0.85"}),
#                         " - ",
#                         html.Span(f"{perdidos_count}", style={"color": "red", "opacity": "0.85"}),
#                         ")"
#                     ], style={"font-size": "0.7em", "opacity": "0.7"})
#                 ], className="stat-value"),
#                 html.P("PJ", className="stat-label")
#             ], className="text-center mb-3"),

#             html.Div([
#                 html.H4(f"{fmt_num(ppp,2)}", className="stat-value"),
#                 html.P("PPP", className="stat-label")
#             ], className="text-center mb-3"),

#             html.Div([
#                 html.H4(f"{fmt_pct01(efg)}", className="stat-value"),
#                 html.P("EFG %", className="stat-label")
#             ], className="text-center mb-3"),

#             html.Div([
#                 html.H4(f"{fmt_pct01(ts)}", className="stat-value"),
#                 html.P("TS %", className="stat-label")
#             ], className="text-center mb-3"),
#         ])
#     )

# @callback(
#     Output('team-logo', 'src'),
#     Input('dropdown-team', 'value')
# )
# def update_team_logo(selected_team):
#     if selected_team:
#         return f"/assets/logos/{selected_team}.png"
#     return "/assets/logos/default.png"

# @callback(
#     Output('jugador-foto', 'src'),
#     Input('dropdown-player', 'value')
# )
# def update_player_photo(selected_player):
#     if selected_player:
#         jugador_info = df[df['Jugadores'] == selected_player]
#         if not jugador_info.empty:
#             ruta_imagen = jugador_info.iloc[0].get('Imagen', None)
#             if ruta_imagen:
#                 return f"/assets/Player_fotos/{ruta_imagen}.png"
#     return "/assets/logos/default.png"

# # =========================
# # GRAPH 1: 3FG %
# # =========================
# @callback(
#     Output('graph_line', 'figure'),
#     [
#         Input('selector_fecha', 'start_date'),
#         Input('selector_fecha', 'end_date'),
#         Input('dropdown-player', 'value'),
#         Input('dropdown-team', 'value'),
#         Input('dropdown-condition', 'value'),
#         Input('dropdown-result', 'value'),
#         Input('dropdown-lastn', 'value'),
#     ]
# )
# def actualizar_graph(fecha_min, fecha_max, selected_player, selected_team, selected_condition, selected_result, selected_lastn):

#     if not selected_player or not selected_team:
#         return empty_fig_message()

#     player_data = apply_filters_boxscore(
#         df_1,
#         team=selected_team,
#         player=selected_player,
#         condition=selected_condition,
#         result=selected_result,
#         last_n=selected_lastn,
#         date_min=fecha_min,
#         date_max=fecha_max,
#     )

#     if player_data.empty:
#         fig = empty_fig_message()
#         fig.update_layout(title=dict(text="Sin datos para esos filtros", x=0.5, y=0.5))
#         return fig

#     player_data = player_data.sort_values(by="Fecha").reset_index(drop=True)
#     player_data["ID"] = np.arange(1, len(player_data) + 1)

#     player_data["3FG_pct_01"] = safe_pct_to_01(player_data["3FG %"]).fillna(0)
#     promedio = float(player_data["3FG_pct_01"].mean())

#     player_data["hover_text"] = (
#         "Fecha: " + player_data["Fecha"].dt.strftime("%d-%m-%Y") + "<br>" +
#         "Condición: " + player_data["Condición"].astype(str) + "<br>" +
#         "Resultado: " + player_data["Resultado"].astype(str) + "<br>" +
#         "Puntos: " + player_data["PTS"].astype(str) + "<br>" +
#         "3FG: " + player_data["3FGM"].astype(str) + "/" + player_data["3FGA"].astype(str) +
#         " - " + (player_data["3FG_pct_01"] * 100).round(1).astype(str) + " %" + "<br>"
#     )

#     fig = go.Figure()

#     fig.add_trace(go.Scatter(
#         x=player_data["ID"],
#         y=player_data["3FG_pct_01"],
#         mode="lines",
#         line=dict(color="blue", width=1),
#         name="Conexión",
#         opacity=0.5,
#         hoverinfo="skip",
#     ))

#     fig.add_trace(go.Scatter(
#         x=player_data["ID"],
#         y=[promedio] * len(player_data),
#         mode="lines",
#         line=dict(dash="dash", color="white"),
#         name=f"Promedio: {promedio*100:.1f} %",
#         opacity=0.5,
#         hoverinfo="skip",
#     ))

#     colores = {"Gano": "green", "Perdio": "red"}
#     for resultado, color in colores.items():
#         subset = player_data[player_data["Resultado"] == resultado]
#         if subset.empty:
#             continue
#         fig.add_trace(go.Scatter(
#             x=subset["ID"],
#             y=subset["3FG_pct_01"],
#             mode="markers",
#             marker=dict(color=color, size=12),
#             text=subset["hover_text"],
#             hoverinfo="text",
#             name=resultado,
#         ))

#     for _, r in player_data.iterrows():
#         fig.add_trace(go.Scatter(
#             x=[r["ID"]],
#             y=[max(r["3FG_pct_01"] - 0.06, -0.02)],
#             mode="text",
#             text=[f"{r['3FG_pct_01']*100:.1f} %"],
#             textfont=dict(color="white", size=14),
#             showlegend=False,
#             hoverinfo="skip",
#         ))

#     if "Opp" in player_data.columns:
#         for _, r in player_data.iterrows():
#             logo_path = f"assets/logos/{r['Opp']}.png"
#             if Path(logo_path).exists():
#                 fig.add_layout_image(
#                     source=f"/{logo_path}",
#                     x=r["ID"],
#                     y=min(r["3FG_pct_01"] + 0.08, 1.02),
#                     xref="x",
#                     yref="y",
#                     xanchor="center",
#                     yanchor="middle",
#                     sizex=0.25,
#                     sizey=0.25,
#                     opacity=1,
#                 )

#     tickvals = np.linspace(0, 1, 6)
#     ticktext = [f"{v*100:.1f} %" for v in tickvals]

#     fig.update_layout(
#         xaxis=dict(title="Partido (ID)", visible=False, automargin=True, showgrid=False, zeroline=False),
#         yaxis=dict(
#             title="3FG %",
#             range=[-0.05, 1.05],
#             tickvals=tickvals,
#             ticktext=ticktext,
#             showgrid=True,
#             zeroline=False,
#         ),
#         margin=dict(l=40, r=20, t=40, b=10),
#         template="plotly_dark",
#         legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
#     )

#     return fig

# # =========================
# # GRAPH 2: PTS
# # =========================
# @callback(
#     Output('graph_line11', 'figure'),
#     [
#         Input('selector_fecha', 'start_date'),
#         Input('selector_fecha', 'end_date'),
#         Input('dropdown-player', 'value'),
#         Input('dropdown-team', 'value'),
#         Input('dropdown-condition', 'value'),
#         Input('dropdown-result', 'value'),
#         Input('dropdown-lastn', 'value'),
#     ]
# )
# def actualizar_graph_1(fecha_min, fecha_max, selected_player, selected_team, selected_condition, selected_result, selected_lastn):

#     if not selected_player or not selected_team:
#         return empty_fig_message()

#     player_data = apply_filters_boxscore(
#         df_1,
#         team=selected_team,
#         player=selected_player,
#         condition=selected_condition,
#         result=selected_result,
#         last_n=selected_lastn,
#         date_min=fecha_min,
#         date_max=fecha_max,
#     )

#     if player_data.empty:
#         fig = empty_fig_message()
#         fig.update_layout(title=dict(text="Sin datos para esos filtros", x=0.5, y=0.5))
#         return fig

#     player_data = player_data.sort_values(by='Fecha').reset_index(drop=True)
#     player_data['ID'] = range(1, len(player_data) + 1)

#     promedio_puntos = player_data['PTS'].mean()

#     player_data['hover_text'] = (
#         'Fecha: ' + player_data['Fecha'].dt.strftime('%d-%m-%Y') + '<br>' +
#         'Condición: ' + player_data['Condición'].astype(str) + '<br>' +
#         'Resultado: ' + player_data['Resultado'].astype(str) + '<br>' +
#         'Puntos: ' + player_data['PTS'].astype(str)
#     )

#     fig = go.Figure()

#     fig.add_trace(go.Scatter(
#         x=player_data['ID'],
#         y=player_data['PTS'],
#         mode='lines',
#         line=dict(color='blue', width=1),
#         name='Conexión',
#         opacity=0.5,
#         hoverinfo='skip'
#     ))

#     fig.add_trace(go.Scatter(
#         x=player_data['ID'],
#         y=[promedio_puntos] * len(player_data),
#         mode='lines',
#         line=dict(dash='dash', color='white'),
#         name=f"Promedio: {promedio_puntos:.2f}",
#         opacity=0.5,
#         hoverinfo='skip'
#     ))

#     colores = {'Gano': 'green', 'Perdio': 'red'}
#     for resultado, color in colores.items():
#         subset = player_data[player_data['Resultado'] == resultado]
#         if subset.empty:
#             continue
#         fig.add_trace(go.Scatter(
#             x=subset['ID'],
#             y=subset['PTS'],
#             mode='markers',
#             marker=dict(color=color, size=12),
#             text=subset['hover_text'],
#             hoverinfo='text',
#             name=resultado
#         ))

#     for _, row in player_data.iterrows():
#         fig.add_trace(go.Scatter(
#             x=[row['ID']],
#             y=[row['PTS'] - 1.5],
#             mode='text',
#             text=[f"{row['PTS']}"],
#             textfont=dict(color="white", size=14),
#             showlegend=False,
#             hoverinfo='skip'
#         ))

#     if "Opp" in player_data.columns:
#         for _, row in player_data.iterrows():
#             logo_path = f"assets/logos/{row['Opp']}.png"
#             if Path(logo_path).exists():
#                 fig.add_layout_image(
#                     source=f"/{logo_path}",
#                     x=row['ID'],
#                     y=row['PTS'] + 2.5,
#                     xref="x",
#                     yref="y",
#                     xanchor="center",
#                     yanchor="middle",
#                     sizex=3,
#                     sizey=3,
#                     opacity=1
#                 )

#     max_pts = float(player_data['PTS'].max()) if not player_data['PTS'].dropna().empty else 0

#     fig.update_layout(
#         xaxis=dict(title="Partido (ID)", visible=False, automargin=True, showgrid=False, zeroline=False),
#         yaxis=dict(
#             title="Puntos",
#             range=[-5, max_pts + 10],
#             tickvals=[i for i in range(0, int(max_pts) + 11, 5)],
#             ticktext=[str(i) for i in range(0, int(max_pts) + 11, 5)],
#             zeroline=False
#         ),
#         margin=dict(l=20, r=20, t=40, b=10),
#         template='plotly_dark',
#         legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
#     )

#     return fig

# # =========================
# # (Opcional) Navbar collapse en móviles
# # =========================
# @callback(
#     Output("navbar-collapse", "is_open"),
#     Input("navbar-toggler", "n_clicks"),
#     prevent_initial_call=True
# )
# def toggle_navbar(n):
#     return bool(n % 2)

# # =========================
# # Run
# # =========================
# # if __name__ == "__main__":
# #     app.run_server(debug=True)

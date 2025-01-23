
from dash import html, dcc, Input, Output, Dash, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path
import plotly.express as px  # Importar Plotly Express
from pathlib import Path


# layout = html.Div([
#     html.H1('Página 2'),
#     html.Div([
#         html.A('Volver a la Página Principal', href='/'),
#         #############################################
#     html.Div(
#     [
#         dbc.Alert("This is a primary alert", color="primary"),
#         dbc.Alert("This is a secondary alert", color="secondary"),
#         dbc.Alert("This is a success alert! Well done!", color="success"),
#         dbc.Alert("This is a warning alert... be careful...", color="warning"),
#         dbc.Alert("This is a danger alert. Scary!", color="danger"),
#         dbc.Alert("This is an info alert. Good to know!", color="info"),
#         dbc.Alert("This is a light alert", color="light"),
#         dbc.Alert("This is a dark alert", color="dark"),
#     ]),
#     ])
# ])

# ##################################################################################################
# df = pd.read_excel("assets/Acumulados.xlsx")
# df_1 = pd.read_excel("assets/boxscore_partidos.xlsx")

# df_1['Fecha'] = pd.to_datetime(df_1['Fecha'], format='%d/%m/%Y', errors='coerce')
# df_1 = df_1.sort_values(by='Fecha', ascending=True)

# layout = dbc.Container([

#     html.Div([
#         html.A('Volver a la Página Principal', href='/')
#     ]),
#     html.H1("Resumen de jugadores por equipos", className='text-center my-4'),

#     # Dropdowns para equipo y jugador
#     dbc.Row([
#         dbc.Col([
#             html.Label("Selecciona un equipo", className='form-label'),
#             dcc.Dropdown(
#                 id='dropdown-team',
#                 options=[
#                     {'label': equipo, 'value': equipo}
#                     for equipo in sorted(df['Team'].unique())
#                 ],
#                 placeholder="Selecciona un equipo",
#                 className="mb-3"
#             ),
#             html.Label("Selecciona un jugador", className='form-label'),
#             dcc.Dropdown(
#                 id='dropdown-player',
#                 placeholder="Selecciona un jugador",
#                 className="mb-3"
#             ),
#         ], width=6),
#         dbc.Col([
#             html.Div(
#                 html.Img(
#                     id='team-logo',
#                     style={
#                         'width': '100%',
#                         'height': 'auto',
#                         'max-height': '150px',
#                         'object-fit': 'contain'
#                     }
#                 ),
#                 style={'text-align': 'center'}
#             )
#         ], width=3),
#         dbc.Col([
#             html.Div(
#                 html.Img(
#                     id='jugador-foto',
#                     style={
#                         'width': '100%',
#                         'height': 'auto',
#                         'max-height': '150px',
#                         'object-fit': 'contain'
#                     }
#                 ),
#                 style={'text-align': 'center'}
#             )
#         ], width=3),
#     ]),

#     # Barra de selección de promedios
#     dbc.Row([
#         dbc.Col([
#             html.Label("Selecciona el tipo de promedio:", className='form-label'),
#             dcc.RadioItems(
#                 id='promedio-selector',
#                 options=[
#                     {'label': 'Promedios Generales', 'value': 'General'},
#                     {'label': 'Promedio Local', 'value': 'Local'},
#                     {'label': 'Promedio Visitante', 'value': 'Visitante'}
#                 ],
#                 value='General',  # Valor por defecto
#                 labelStyle={'display': 'block'},
#                 className="mb-3"
#             )
#         ])
#     ], className='my-4'),

#     # Cards para métricas
#     dbc.Row([
#         dbc.Col(dbc.Card(id='points-card1', body=True, className="dashboard-card"), width=3),
#         dbc.Col(dbc.Card(id='rebound-card1', body=True, className="dashboard-card"), width=3),
#         dbc.Col(dbc.Card(id='assists-card1', body=True, className="dashboard-card"), width=3),
#         dbc.Col(dbc.Card(id='min-card1', body=True, className="dashboard-card"), width=3),
#     ], class_name="my-4 g-3"),

#     html.Div(
#     [
#         dbc.Alert("This is a primary alert", color="primary"),
#         dbc.Alert("This is a secondary alert", color="secondary"),
#         dbc.Alert("This is a success alert! Well done!", color="success"),
#         dbc.Alert("This is a warning alert... be careful...", color="warning"),
#         dbc.Alert("This is a danger alert. Scary!", color="danger"),
#         dbc.Alert("This is an info alert. Good to know!", color="info"),
#         dbc.Alert("This is a light alert", color="light"),
#         dbc.Alert("This is a dark alert", color="dark"),
#     ]),

# ], fluid=True)




# @callback(
#     [
#         Output('points-card1', 'children'),
#         Output('rebound-card1', 'children'),
#         Output('assists-card1', 'children'),
#         Output('min-card1', 'children')
#     ],
#     [
#         Input('dropdown-player', 'value'),
#         Input('promedio-selector', 'value')  # Nueva entrada para el selector
#     ]
# )
# def update_player_info(selected_player, promedio_seleccion):
#     if not selected_player:
#         return (
#             dbc.CardBody([html.H3("N/A", className="stat-value"), html.P("Anotación", className="stat-label")]),
#             dbc.CardBody([html.H3("N/A", className="stat-value"), html.P("Rebotes", className="stat-label")]),
#             dbc.CardBody([html.H3("N/A", className="stat-value"), html.P("Asistencias", className="stat-label")]),
#             dbc.CardBody([html.H3("N/A", className="stat-value"), html.P("Minutos", className="stat-label")])
#         )

#     # Filtrar los datos del jugador seleccionado
#     player_data = df_1[df_1['Jugadores'] == selected_player]

#     # Calcular promedios generales (sin filtro de condición)
#     general_points = player_data['PTS'].mean() if not player_data.empty else 0
#     general_rebounds = player_data['RT'].mean() if not player_data.empty else 0
#     general_assists = player_data['AST'].mean() if not player_data.empty else 0
#     general_minutes = player_data['MIN'].mean() if not player_data.empty else 0

#     # Filtrar datos según la selección
#     if promedio_seleccion == 'Local':
#         player_data = player_data[player_data['Condición'] == 'Local']
#     elif promedio_seleccion == 'Visitante':
#         player_data = player_data[player_data['Condición'] == 'Visita']

#     # Calcular métricas actuales según la selección
#     points = player_data['PTS'].mean() if not player_data.empty else 0
#     rebounds = player_data['RT'].mean() if not player_data.empty else 0
#     assists = player_data['AST'].mean() if not player_data.empty else 0
#     minutes = player_data['MIN'].mean() if not player_data.empty else 0

#     # Función para determinar la flecha
#     def get_arrow_html(value, general_value):
#         if value > general_value:
#             return html.Span("⬆", style={'color': 'green', 'margin-left': '10px'})
#         elif value < general_value:
#             return html.Span("⬇", style={'color': 'red', 'margin-left': '10px'})
#         return html.Span("➡", style={'color': 'gray', 'margin-left': '10px'})

#     # Actualizar cards con flechas
#     return (
#         dbc.CardBody([
#             html.H2("PUNTOS", className="card-title"),
#             html.Div([
#                 html.H3(f"{points:.2f}", className="stat-value1"),
#                 get_arrow_html(points, general_points),
#                 html.P("Promedio", className="stat-label1")
#             ])
#         ]),
#         dbc.CardBody([
#             html.H2("REBOTES", className="card-title"),
#             html.Div([
#                 html.H3(f"{rebounds:.2f}", className="stat-value1"),
#                 get_arrow_html(rebounds, general_rebounds),
#                 html.P("Promedio", className="stat-label1")
#             ])
#         ]),
#         dbc.CardBody([
#             html.H2("ASISTENCIAS", className="card-title"),
#             html.Div([
#                 html.H3(f"{assists:.2f}", className="stat-value1"),
#                 get_arrow_html(assists, general_assists),
#                 html.P("Promedio", className="stat-label1")
#             ])
#         ]),
#         dbc.CardBody([
#             html.H2("MINUTOS", className="card-title"),
#             html.Div([
#                 html.H3(f"{minutes:.2f}", className="stat-value1"),
#                 get_arrow_html(minutes, general_minutes),
#                 html.P("Promedio", className="stat-label1")
#             ])
#         ])
#     )


from dash import html, dcc, Input, Output, Dash, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from fpdf import FPDF
import plotly.graph_objs as go


# Cargar datos
# df contiene información general, df_1 tiene estadísticas por partido
df = pd.read_excel("assets/Acumulados.xlsx")
df_1 = pd.read_excel("assets/boxscore_partidos.xlsx")

df_1['Fecha'] = pd.to_datetime(df_1['Fecha'], format='%d/%m/%Y', errors='coerce')
df_1 = df_1.sort_values(by='Fecha', ascending=True)

layout = dbc.Container([

    html.Div([
        html.A('Volver a la Página Principal', href='/')
    ]),
    html.H1("Resumen de jugadores por equipos", className='text-center my-4'),

    # Dropdowns para equipo y jugador
    dbc.Row([
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
    ]),

    # Tabs para promedios
    dbc.Tabs([
        dbc.Tab(label="Promedio", tab_id="General"),
        dbc.Tab(label="Local", tab_id="Local"),
        dbc.Tab(label="Visitante", tab_id="Visitante"),
    ], id="tabs-selector", active_tab="General"),

    # Cards para métricas
    dbc.Row([
        dbc.Col(dbc.Card(id='points-card1', body=True, className="dashboard-card"), width=3),
        dbc.Col(dbc.Card(id='rebound-card1', body=True, className="dashboard-card"), width=3),
        dbc.Col(dbc.Card(id='assists-card1', body=True, className="dashboard-card"), width=3),
        dbc.Col(dbc.Card(id='min-card1', body=True, className="dashboard-card"), width=3),
    ], class_name="my-4 g-3"),

    # Botón para exportar a PDF
    html.Div([
        dbc.Button("Exportar a PDF", id="export-pdf", color="primary", className="mt-3")
    ]),

], fluid=True)


@callback(
    [
        Output('points-card1', 'children'),
        Output('rebound-card1', 'children'),
        Output('assists-card1', 'children'),
        Output('min-card1', 'children')
    ],
    [
        Input('dropdown-player', 'value'),
        Input('tabs-selector', 'active_tab')
    ]
)
def update_player_info(selected_player, active_tab):
    if not selected_player:
        return (
            dbc.CardBody([html.H3("N/A", className="stat-value1"), html.P("Anotación", className="stat-label1")]),
            dbc.CardBody([html.H3("N/A", className="stat-value1"), html.P("Rebotes", className="stat-label1")]),
            dbc.CardBody([html.H3("N/A", className="stat-value1"), html.P("Asistencias", className="stat-label1")]),
            dbc.CardBody([html.H3("N/A", className="stat-value1"), html.P("Minutos", className="stat-label1")])
        )

    # Filtrar los datos del jugador seleccionado
    player_data = df_1[df_1['Jugadores'] == selected_player]

    # Calcular promedios generales (sin filtro de condición)
    general_points = player_data['PTS'].mean() if not player_data.empty else 0
    general_rebounds = player_data['RT'].mean() if not player_data.empty else 0
    general_assists = player_data['AST'].mean() if not player_data.empty else 0
    general_minutes = player_data['MIN'].mean() if not player_data.empty else 0

    # Filtrar datos según la pestaña activa
    if active_tab == "Local":
        player_data = player_data[player_data['Condición'] == 'Local']
    elif active_tab == "Visitante":
        player_data = player_data[player_data['Condición'] == 'Visita']

    # Calcular métricas actuales según la selección
    points = player_data['PTS'].mean() if not player_data.empty else 0
    rebounds = player_data['RT'].mean() if not player_data.empty else 0
    assists = player_data['AST'].mean() if not player_data.empty else 0
    minutes = player_data['MIN'].mean() if not player_data.empty else 0

    # Función para determinar la flecha
    def get_arrow_html(value, general_value):
        if value > general_value:
            return html.Span("⬆", style={'color': 'green', 'margin-left': '10px'})
        elif value < general_value:
            return html.Span("⬇", style={'color': 'red', 'margin-left': '10px'})
        return html.Span("➡", style={'color': 'gray', 'margin-left': '10px'})

    # Actualizar cards con flechas
    return (
        dbc.CardBody([
            html.H2("PUNTOS", className="card-title"),
            html.Div([
                html.H3(f"{points:.2f}", className="stat-value1"),
                get_arrow_html(points, general_points),
                html.P("Promedio", className="stat-label1")
            ])
        ]),
        dbc.CardBody([
            html.H2("REBOTES", className="card-title"),
            html.Div([
                html.H3(f"{rebounds:.2f}", className="stat-value1"),
                get_arrow_html(rebounds, general_rebounds),
                html.P("Promedio", className="stat-label1")
            ])
        ]),
        dbc.CardBody([
            html.H2("ASISTENCIAS", className="card-title"),
            html.Div([
                html.H3(f"{assists:.2f}", className="stat-value1"),
                get_arrow_html(assists, general_assists),
                html.P("Promedio", className="stat-label1")
            ])
        ]),
        dbc.CardBody([
            html.H2("MINUTOS", className="card-title"),
            html.Div([
                html.H3(f"{minutes:.2f}", className="stat-value1"),
                get_arrow_html(minutes, general_minutes),
                html.P("Promedio", className="stat-label1")
            ])
        ])
    )

from fpdf import FPDF

@callback(
    Output("export-pdf", "n_clicks"),
    [
        Input("export-pdf", "n_clicks"),
        Input('dropdown-player', 'value'),
        Input('tabs-selector', 'active_tab'),
    ]
)
def export_to_pdf(n_clicks, selected_player, active_tab):
    if n_clicks and selected_player:
        # Filtrar los datos del jugador seleccionado
        player_data = df_1[df_1['Jugadores'] == selected_player]
        
        # Calcular promedios generales
        general_points = player_data['PTS'].mean() if not player_data.empty else 0
        general_rebounds = player_data['RT'].mean() if not player_data.empty else 0
        general_assists = player_data['AST'].mean() if not player_data.empty else 0
        general_minutes = player_data['MIN'].mean() if not player_data.empty else 0

        # Filtrar datos según la pestaña activa
        if active_tab == "Local":
            player_data = player_data[player_data['Condición'] == 'Local']
        elif active_tab == "Visitante":
            player_data = player_data[player_data['Condición'] == 'Visita']

        # Calcular métricas actuales según la selección
        points = player_data['PTS'].mean() if not player_data.empty else 0
        rebounds = player_data['RT'].mean() if not player_data.empty else 0
        assists = player_data['AST'].mean() if not player_data.empty else 0
        minutes = player_data['MIN'].mean() if not player_data.empty else 0

        # Crear el PDF
        pdf = FPDF()
        pdf.add_page()

        # Usar la fuente Unicode incluida en el sistema
        # pdf.add_font("LiberationSans", "", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", uni=True)
        # pdf.set_font("LiberationSans", size=12)


        pdf.add_font("Arial", "", "C:\\Windows\\Fonts\\arial.ttf", uni=True)
        pdf.set_font("Arial", size=12)


        # Título
        pdf.cell(200, 10, txt=f"Reporte de Jugador: {selected_player}", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Tab Activa: {active_tab}", ln=True, align='C')

        # Espaciado
        pdf.ln(10)

        # Función para determinar la flecha
        def get_arrow(value, general_value):
            if value > general_value:
                return "⬆"
            elif value < general_value:
                return "⬇"
            return "➡"

        # Exportar métricas
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Resumen de Métricas", ln=True, align='L')
        pdf.ln(5)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Puntos: {points:.2f} {get_arrow(points, general_points)}", ln=True)
        pdf.cell(0, 10, f"Rebotes: {rebounds:.2f} {get_arrow(rebounds, general_rebounds)}", ln=True)
        pdf.cell(0, 10, f"Asistencias: {assists:.2f} {get_arrow(assists, general_assists)}", ln=True)
        pdf.cell(0, 10, f"Minutos: {minutes:.2f} {get_arrow(minutes, general_minutes)}", ln=True)

        # Guardar el PDF
        pdf.output("Reporte_Jugador.pdf")

    return None

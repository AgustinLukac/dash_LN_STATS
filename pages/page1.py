
import dash
from app import app
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime, timedelta
from dash import dash_table
import dash_ag_grid as dag


df = pd.read_excel("assets/Acumulados.xlsx")
fecha_fin= datetime.now()
fecha_inicio = fecha_fin -timedelta(days=180)


# Crear datos de ejemplo de jugadores
jugadores_data = {
    'nombre': ['Lionel Messi', 'Cristiano Ronaldo', 'Robert Lewandowski', 
               'Kevin De Bruyne', 'Mohamed Salah', 'Karim Benzema', 
               'Kylian Mbappé', 'Erling Haaland', 'Luka Modric', 'Vinícius Jr'],
    'posicion': ['Delantero', 'Delantero', 'Delantero', 
                 'Mediocampista', 'Delantero', 'Delantero',
                 'Delantero', 'Delantero', 'Mediocampista', 'Delantero'],
    'equipo': ['Inter Miami', 'Al Nassr', 'Barcelona', 
               'Manchester City', 'Liverpool', 'Real Madrid',
               'PSG', 'Manchester City', 'Real Madrid', 'Real Madrid'],
    'partidos_jugados': [28, 30, 25, 27, 29, 26, 28, 29, 24, 27],
    'goles': [25, 28, 22, 10, 19, 20, 30, 35, 5, 18],
    'asistencias': [15, 8, 5, 18, 10, 7, 12, 5, 12, 9],
    'minutos_jugados': [2520, 2700, 2250, 2430, 2610, 2340, 2520, 2610, 2160, 2430],
    'tarjetas_amarillas': [2, 3, 1, 4, 2, 3, 4, 1, 5, 3],
    'tarjetas_rojas': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    'efectividad_gol': [0.89, 0.93, 0.88, 0.37, 0.66, 0.77, 1.07, 1.21, 0.21, 0.67]
}

df1 = pd.DataFrame(jugadores_data)

# Configuración de columnas
columnDefs = [
    {
        'headerName': 'Jugador',
        'field': 'nombre',
        'checkboxSelection': True,
        'headerCheckboxSelection': True,
        'pinned': 'left',
        'filter': 'agTextColumnFilter',
        'minWidth': 180
    },
    {
        'headerName': 'Posición',
        'field': 'posicion',
        'filter': 'agSetColumnFilter'
    },
    {
        'headerName': 'Equipo',
        'field': 'equipo',
        'filter': 'agSetColumnFilter'
    },
    {
        'headerName': 'Estadísticas',
        'children': [
            {
                'headerName': 'PJ',
                'field': 'partidos_jugados',
                'type': 'numericColumn',
                'filter': 'agNumberColumnFilter',
                'width': 80
            },
            {
                'headerName': 'Goles',
                'field': 'goles',
                'type': 'numericColumn',
                'filter': 'agNumberColumnFilter',
                'width': 90,
                'cellStyle': {
                    'styleConditions': [
                        {
                            'condition': 'params.value > 25',
                            'style': {'color': 'white', 'backgroundColor': '#2ecc71'}
                        }
                    ]
                }
            },
            {
                'headerName': 'Asist.',
                'field': 'asistencias',
                'type': 'numericColumn',
                'filter': 'agNumberColumnFilter',
                'width': 90
            }
        ]
    },
    {
        'headerName': 'Minutos',
        'field': 'minutos_jugados',
        'type': 'numericColumn',
        'valueFormatter': {'function': "d3.format(',')"}, 
        'filter': 'agNumberColumnFilter'
    },
    {
        'headerName': 'Disciplina',
        'children': [
            {
                'headerName': 'TA',
                'field': 'tarjetas_amarillas',
                'type': 'numericColumn',
                'width': 80,
                'cellStyle': {'backgroundColor': '#fff9c4'}
            },
            {
                'headerName': 'TR',
                'field': 'tarjetas_rojas',
                'type': 'numericColumn',
                'width': 80,
                'cellStyle': {'backgroundColor': '#ffcdd2'}
            }
        ]
    },
    {
        'headerName': 'Efect. Gol',
        'field': 'efectividad_gol',
        'type': 'numericColumn',
        'valueFormatter': {'function': "d3.format('.2f')"},
        'cellStyle': {
            'styleConditions': [
                {
                    'condition': 'params.value > 1.0',
                    'style': {'color': 'white', 'backgroundColor': '#3498db'}
                }
            ]
        }
    }
]

# Configuración de la grid
gridOptions = {
    'columnDefs': columnDefs,
    'rowData': df.to_dict('records'),
    'enableSorting': True,
    'enableFilter': True,
    'enableColResize': True,
    'pagination': True,
    'paginationPageSize': 10,
    'rowSelection': 'multiple',
    'rowMultiSelectWithClick': True,
    'defaultColDef': {
        'resizable': True,
        'sortable': True,
        'filter': True,
        'minWidth': 100,
    },
    'sideBar': True
}



layout = html.Div([

    html.Div([
        html.A('Volver a la Página Principal', href='/')
    ]),

    #############################################
    html.Ul([
        html.Li(html.A("Estadísticas Equipo", href="http:/")),
        html.Li("Estadísticas Campeonato"),
        html.Li("Estadísticas Jugadores"),
        html.Li("Estadísticas Equipos"),
        html.Li("Estadísticas Partidos"),
        html.Li("Estadísticas Alineaciones")
    ]),

    #############################################
    html.Div(
    [
        dbc.Spinner(color="primary", type="grow"),
        dbc.Spinner(color="secondary", type="grow"),
        dbc.Spinner(color="success", type="grow"),
        dbc.Spinner(color="warning", type="grow"),
        dbc.Spinner(color="danger", type="grow"),
        dbc.Spinner(color="info", type="grow"),
        dbc.Spinner(color="light", type="grow"),
        dbc.Spinner(color="dark", type="grow"),
    ]),

    #############################################
    dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="My Navbar",
    brand_href="#",
    color="primary",
    dark=True,),
    #############################################
    html.H1('Estadísticas de Jugadores', className="mt-4"),
    #############################################
    dbc.Carousel(
    items=[
        {"key": "1", "src": "assets/VILDOZA.png","header": "With header ",},
        {"key": "2", "src": "assets/STENTA.png","header": "With header ",},
        {"key": "3", "src": "assets/CUELLO.png","header": "With header ",},
    ],
    variant="dark",
    controls=True,
    indicators=True,
    style={"width": "15%", "margin": "0 auto"}),

    #############################################
    html.Div(
    [
        dbc.Alert("This is a primary alert", color="primary"),
        dbc.Alert("This is a secondary alert", color="secondary"),
        dbc.Alert("This is a success alert! Well done!", color="success"),
        dbc.Alert("This is a warning alert... be careful...", color="warning"),
        dbc.Alert("This is a danger alert. Scary!", color="danger"),
        dbc.Alert("This is an info alert. Good to know!", color="info"),
        dbc.Alert("This is a light alert", color="light"),
        dbc.Alert("This is a dark alert", color="dark"),
    ]),
    
    
    #############################################
    dbc.Card(
    [
        dbc.CardImg(src="assets/STENTA.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},),

    ###############################################
    dbc.Container([
        dbc.Navbar([
            dbc.NavbarBrand("Club Atletico Fantasía"),
            dbc.Nav([

                dbc.NavItem(dbc.NavLink("Inicio", href="/")),
                dbc.NavItem(dbc.NavLink("     Estadísticas", href="/")),
                dbc.NavItem(dbc.NavLink("     Jugadores", href="/")),

            ]),
            

        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Métricas Claves"),
                dbc.CardBody([

                    # Conteido de Métricas
                    html.H5("Juan Pérez", className="card-title"),
                    html.P("Estadísticas Temporada 2024/25"),
                    dbc.ListGroup([
                        dbc.ListGroupItem("Goles: 15"),
                        dbc.ListGroupItem("Asistencias: 20"),
                        dbc.ListGroupItem("Rebotes: 10")
                    ])
                ])
            ]), width=4

            ),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Gráficos de Rendimiento"),
                dbc.CardBody([
                    # Contenido de Métricas
                ])
            ]), width=8),


        ])
    ]),
    




    #############################################
    dbc.Row([  # Las columnas deben estar dentro de una fila
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src="assets/VILDOZA.png", top=True,style={
                        "opacity": "0.8",  # Transparencia
                        "width": "40%",   # Tamaño reducido al 20% del contenedor
                        "margin": "0 auto",  # Centrar la imagen horizontalmente
                        "background-color": "transparent"  # Asegurar que el fondo sea transparente
                    }),
                dbc.CardBody([
                    html.H2('JOSÉ VILDOZA', className="card-title text-center"),
                    html.P('Nombre: Juan Mateo', className="card-text"),
                    html.P('Posición: Alero', className="card-text"),
                    html.Button('Ver Más', id="boton-basico")
                ])
            ])
        ], md=4),

        dbc.Col([
            dbc.Card([
                dbc.CardImg(src="assets/STENTA.png", top=True,style={
                        "opacity": "0.8",  # Transparencia
                        "width": "40%",   # Tamaño reducido al 20% del contenedor
                        "margin": "0 auto",  # Centrar la imagen horizontalmente
                        "background-color": "transparent"  # Asegurar que el fondo sea transparente
                    }),
                dbc.CardBody([
                    html.H2('NICOLÁS STENTA', className="card-title"),
                    html.P('Nombre: Juan Mateo', className="card-text"),
                    html.P('Posición: Alero', className="card-text"),
                    html.Button('Ver Más', id="boton-basico_2")
                ])
            ])
        ], md=4),

        dbc.Col([
            dbc.Card([
                dbc.CardImg(src="assets/CUELLO.png", top=True,style={
                        "opacity": "0.8",  # Transparencia
                        "width": "40%",   # Tamaño reducido al 20% del contenedor
                        "margin": "0 auto",  # Centrar la imagen horizontalmente
                        "background-color": "transparent"  # Asegurar que el fondo sea transparente
                    }),
                dbc.CardBody([
                    html.H2('MARTIN CUELLO', className="card-title text-center"),
                    html.P('Nombre: Juan Mateo', className="card-text"),
                    html.P('Posición: Alero', className="card-text"),
                    html.Button('Ver Más', id="boton-basico_3")
                ])
            ])
        ], md=4)
    ], className="mt-4"),



    ############################################

    html.Div([

        dbc.NavbarSimple(

            children=[

                dbc.Input(
                    id="filter-input",
                    type="text",
                    placeholder="Filtrar por nombre...",
                    debounce=True,),
                dbc.Select(
                    id="filter-select",
                    options=[
                        {"label": "Todos", "value": "Todos"},
                        {"label": "BOCA", "value": "BOCA"},
                        {"label": "OBERA", "value": "OBERA"},
                        {"label": "QUIMSA", "value": "QUIMSA"},
                        {"label": "FERRO", "value": "FERRO"},
                    ],
                    value="Todos",  # Valor por defecto
                    placeholder="Filtrar por equipo",
                ),
            ],
            brand="Filtro de Tabla",
            brand_href="#",
            color="primary",
            dark=True,)]),
    ##############################
    html.Div([
        html.Label("Filtrar por mínimo de triples convertidos (3FGM):"),
        dcc.Slider(
            id="3fgm-slider",
            min=df["3FGM"].min(),  # Valor mínimo en la columna
            max=df["3FGM"].max(),  # Valor máximo en la columna
            step=1,
            value=df["3FGM"].min(),  # Valor inicial
            marks={i: str(i) for i in range(int(df["3FGM"].min()), int(df["3FGM"].max()) + 1, 1)},
        ),
    ], style={"padding": "20px"}),

    ##################################

    dcc.Slider(
        id= 'rango-fechas',
        min=0,
        max=100,
        step=1,
        value=50,
        marks={0:'Inicio', 50 :'Medio', 100 : 'Fin'}
    ),




    dcc.DatePickerRange(
    id='selector de partidos',
    start_date = fecha_inicio,
    end_date = fecha_fin,
    display_format = 'DD/MM/YYYY'),


    ###############################
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"},
    ),

    ###########################################


    ###########################################

    dash_table.DataTable(
    id="data-table1",
    columns=[{"name": i, "id": i} for i in ["Jugadores", "Team", "#", "MIN", "PTS", "3FGM", "PPP"]],
    data=df[["Jugadores", "Team", "#", "MIN", "PTS", "3FGM", "PPP"]].to_dict("records"),
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "center"},
    sort_action="native",
    filter_action="native",
    style_header={
        "backgroundColor": "#D4F1F4",
        "fontWeight": "bold",
        "textAlign": "center",
    },
    style_data_conditional=[
        {
            "if": {"filter_query": "{PTS} > 10", "column_id": "PTS"},
            "backgroundColor": "#FFDDC1",
            "color": "black",
        },
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#F9F9F9",
        },
        {
            "if": {"state": "active"},
            "backgroundColor": "#BEE3DB",
            "border": "1px solid black",
        },
    ],
    column_selectable="single",
    ),


     dag.AgGrid(
        id='grid-deportes',
        columnDefs=columnDefs,
        rowData=df1.to_dict('records'),
        dashGridOptions=gridOptions,
        style={'height': '600px'},
        className="ag-theme-alpine"
    )

    





])



# Callback para filtrar la tabla
@app.callback(
    [
        Output("data-table", "data"),
        Output("data-table1", "data"),
    ],
    [
        Input("filter-input", "value"),
        Input("filter-select", "value"),
        Input("3fgm-slider", "value"),
    ],
)
def update_table(input_value, select_value, min_3fgm):
    filtered_df = df

    # Filtrar por nombre
    if input_value:
        filtered_df = filtered_df[
            filtered_df["Jugadores"].str.contains(input_value, case=False, na=False)
        ]

    # Filtrar por equipo
    if select_value and select_value != "Todos":
        filtered_df = filtered_df[filtered_df["Team"] == select_value]

    # Filtrar por valor mínimo de 3FGM
    filtered_df = filtered_df[filtered_df["3FGM"] >= min_3fgm]

    return filtered_df.to_dict("records"), filtered_df.to_dict("records")



if __name__ == '__main__':
    app.run_server(debug=True)

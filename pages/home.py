from app import app  # Si necesitas referenciar la app, puedes hacerlo
from dash import html

layout = html.Div([
    html.H1("Bienvenido a la Página Principal"),

    html.Div([
        
        html.Div([
        html.A([
            html.Img(
                src='/assets/VILDOZA.png',
                style={
                    'border-radius': '15px',
                    'width': '200px',
                    'height': 'auto',
                    'border': '2px solid #ccc',
                    'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
                    'margin': '20px'
                }
            )
        ], href="/page3")  # El hipervínculo a la página 3
    ], style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center'
    }),



        html.Img(
            src='/assets/STENTA.png',  # Asegúrate que la extensión coincida con tu archivo
            style={
                'border-radius': '15px',  # Bordes redondeados
                'width': '200px',  # Puedes ajustar el tamaño
                'height': 'auto',
                'border': '2px solid #ccc',  # Borde gris claro
                'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',  # Sombra sutil
                'margin': '20px'  # Espacio alrededor de la imagen
            }
        )
    ], style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center'
    }),




    html.Div([
        html.A("Ir a Página 1", href="/page1"),
        html.Br(),
        html.A("Ir a Página 2", href="/page2"),
        html.Br(),
        html.A("Ir a Página 3", href="/page3"),
        html.Br(),
        html.A("Ir a Página 4", href="/page4")
    ])
])

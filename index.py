from dash import dcc, html
from dash.dependencies import Input, Output
from app import app
from pages import home, page1, page2, page3, page4  # Importa las páginas

# Define el layout principal con enlaces a cada página
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Maneja la URL
    html.Div(id='page-content')  # Aquí se carga el contenido dinámico
])

# Callback para actualizar el contenido según la URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    elif pathname == '/page3':
        return page3.layout
    elif pathname == '/page4':
        return page4.layout
    else:
        return home.layout  # Página por defecto

if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, 
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # Estilo de Bootstrap
    suppress_callback_exceptions=True,  # Permite excepciones en callbacks fuera del archivo principal
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}  # Adaptación móvil
    ]
)
server = app.server  # Esto es útil para despliegues

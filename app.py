# app.py
from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1("Dashboard de Processos Judiciais", style={'textAlign': 'center'}),

    html.Div([
        dcc.Link("Página 1", href="/", style={"marginRight": "15px"}),
        dcc.Link("Página 2", href="/pagina2", style={"marginRight": "15px"}),
        dcc.Link("Página 3", href="/pagina3", style={"marginRight": "15px"}),
        dcc.Link("Página 4", href="/pagina4")
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)

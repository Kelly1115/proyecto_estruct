import dash
from dash import dcc, html, Input, Output
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Importa tus funciones de otras fases
from carga_datos import cargar_datos_excel
from Crear_grafo import construir_grafo
from riesgo import calcular_riesgos_y_montos, ordenar_bancos_por_monto
from Busqueda import buscar_conexiones_bfs

# Cargar y procesar datos al inicio
df = cargar_datos_excel("base_de_datos.xlsx")
G = construir_grafo(df)
montos, riesgos = calcular_riesgos_y_montos(G)
ranking = ordenar_bancos_por_monto(montos)
bancos = list(G.nodes)

# Función para graficar
def generar_figura_grafo(grafo, riesgos):
    pos = nx.spring_layout(grafo, seed=42)
    edge_x, edge_y = [], []
    for edge in grafo.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=1, color='#888'),
                            hoverinfo='none',
                            mode='lines')

    node_x, node_y, node_color, node_text = [], [], [], []
    for node in grafo.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        riesgo = riesgos.get(node, 'Bajo')
        color = {'Bajo': 'green', 'Medio': 'orange', 'Alto': 'red'}.get(riesgo, 'gray')
        node_color.append(color)
        node_text.append(f"{node} - Riesgo: {riesgo}")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        textposition="bottom center",
        text=node_text,
        hoverinfo='text',
        marker=dict(color=node_color, size=30, line=dict(width=2))
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Red de Préstamos Interbancarios',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))
    return fig

# Crear la app de Dash
app = dash.Dash(__name__)
app.title = "Análisis Interbancario"

# Layout de la página
app.layout = html.Div([
    html.H1("Análisis de Préstamos Interbancarios", style={'textAlign': 'center'}),

    dcc.Graph(id='grafo-bancos', figure=generar_figura_grafo(G, riesgos)),

    html.Div([
        html.Label("Selecciona un banco:"),
        dcc.Dropdown(options=[{"label": b, "value": b} for b in bancos],
                     id='dropdown-banco',
                     placeholder="Elige un banco")
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div(id='resultado-riesgo', style={'textAlign': 'center', 'marginTop': '20px', 'fontSize': '20px'}),

    html.Div(id='resultado-bfs', style={'textAlign': 'center', 'marginTop': '10px'}),

    html.H2("Ranking de Bancos por Monto Prestado", style={'textAlign': 'center', 'marginTop': '40px'}),
    html.Table([
        html.Thead(html.Tr([html.Th("Banco"), html.Th("Monto Total Prestado")])),
        html.Tbody([
            html.Tr([html.Td(banco), html.Td(f"${monto:,.2f}")]) for banco, monto in ranking
        ])
    ], style={'margin': 'auto', 'border': '1px solid black', 'width': '50%'})
])

# Callback para mostrar riesgo y BFS desde banco seleccionado
@app.callback(
    Output('resultado-riesgo', 'children'),
    Output('resultado-bfs', 'children'),
    Input('dropdown-banco', 'value')
)
def actualizar_info_banco(banco):
    if banco is None:
        return "", ""

    riesgo = riesgos.get(banco, 'Desconocido')
    conexiones = buscar_conexiones_bfs(G, banco)
    conexiones_texto = ", ".join(conexiones) if conexiones else "Sin conexiones encontradas"

    return f"Nivel de riesgo: {riesgo}", f"Bancos conectados desde {banco}: {conexiones_texto}"

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
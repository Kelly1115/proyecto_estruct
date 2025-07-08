import networkx as nx
from carga_datos import cargar_datos_excel
from Crear_grafo import construir_grafo

def buscar_conexiones_bfs(grafo, banco_inicial):
    """
    Realiza una búsqueda en anchura (BFS) desde el banco_inicial en el grafo.
    Retorna una lista de bancos conectados (alcanzables) desde banco_inicial.
    Si el banco no existe en el grafo, retorna una lista vacía.
    """
    if banco_inicial not in grafo.nodes:
        return []

    bfs_resultado = nx.bfs_tree(grafo, banco_inicial)
    bancos_conectados = list(bfs_resultado.nodes)
    bancos_conectados.remove(banco_inicial)
    return bancos_conectados

if __name__ == "__main__":
    # Cargar datos reales desde Excel
    df = cargar_datos_excel("base_de_datos.xlsx")
    if df is not None:
        grafo = construir_grafo(df)
        # Puedes cambiar el banco inicial por el que quieras analizar
        banco_inicial = df['Banco_Origen'].iloc[0]  # O escribe el nombre de un banco, por ejemplo: 'Banco Pichincha'
        resultado = buscar_conexiones_bfs(grafo, banco_inicial)
        print(f"Bancos conectados desde {banco_inicial}:", resultado)
    else:
        print("No se pudieron cargar los datos.")
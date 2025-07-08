import networkx as nx

def construir_grafo(df):
    """
    Recibe un DataFrame con columnas: Banco_Origen, Banco_Destino, Monto, Fecha
    Devuelve un grafo dirigido donde:
      - Los nodos son bancos
      - Las aristas representan préstamos (de Banco_Origen a Banco_Destino)
      - El atributo 'monto' guarda el valor del préstamo
      - El atributo 'fecha' guarda la fecha del préstamo
    
    """
    G = nx.DiGraph()

    for _, fila in df.iterrows():
        banco_origen = fila['Banco_Origen']
        banco_destino = fila['Banco_Destino']
        monto = fila['Monto']
        fecha = fila['Fecha']

        # Si ya existe la arista, acumulamos el monto y podemos guardar la última fecha (o lista)
        if G.has_edge(banco_origen, banco_destino):
            G[banco_origen][banco_destino]['monto'] += monto
            # Opcional: guardar fechas en lista
            G[banco_origen][banco_destino]['fechas'].append(fecha)
        else:
            G.add_edge(banco_origen, banco_destino, monto=monto, fechas=[fecha])

    return G

# Para prueba rápida
if __name__ == "__main__":
    import pandas as pd
    from carga_datos import cargar_datos_excel
    archivo = "base_de_datos.xlsx"
    df = cargar_datos_excel(archivo)
    grafo = construir_grafo(df)

    print("Nodos (bancos):", grafo.nodes())
    print("Aristas (préstamos):")
    for u, v, data in grafo.edges(data=True):
        print(f"{u} -> {v}: monto = {data['monto']}, fechas = {data['fechas']}")

from carga_datos import cargar_datos_excel
from Crear_grafo import construir_grafo

def calcular_riesgos_y_montos(grafo):
    """
    Calcula el monto total prestado por cada banco y asigna un nivel de riesgo.
    Parámetros:
      - grafo: NetworkX DiGraph con atributo 'monto' en cada arista.
    Retorna:
      - montos_prestados: dict {banco: monto_total_prestado}
      - riesgos: dict {banco: 'Bajo'/'Medio'/'Alto'}
    """
    montos_prestados = {}
    riesgos = {}

    for banco in grafo.nodes():
        total_prestado = 0
        for _, destino, data in grafo.out_edges(banco, data=True):
            total_prestado += data.get('monto', 0)
        montos_prestados[banco] = total_prestado

    # Definimos umbrales para riesgo (puedes ajustar según tus datos)
    umbral_bajo = 500000
    umbral_alto = 1000000

    for banco, monto in montos_prestados.items():
        if monto < umbral_bajo:
            riesgos[banco] = 'Bajo'
        elif monto < umbral_alto:
            riesgos[banco] = 'Medio'
        else:
            riesgos[banco] = 'Alto'

    return montos_prestados, riesgos

def ordenar_bancos_por_monto(montos_prestados):
    """
    Ordena bancos de mayor a menor según monto prestado.
    Parámetros:
      - montos_prestados: dict {banco: monto}
    Retorna:
      - lista de tuplas [(banco, monto), ...] ordenada descendente
    """
    return sorted(montos_prestados.items(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    # Cargar datos reales desde Excel
    df = cargar_datos_excel("base_de_datos.xlsx")
    if df is not None:
        grafo = construir_grafo(df)

        montos, riesgos = calcular_riesgos_y_montos(grafo)
        print("Montos prestados:", montos)
        print("Riesgos asignados:", riesgos)

        ranking = ordenar_bancos_por_monto(montos)
        print("Ranking bancos por monto prestado:")
        for banco, monto in ranking:
            print(f"{banco}: ${monto}")
    else:
        print("No se pudieron cargar los datos.")
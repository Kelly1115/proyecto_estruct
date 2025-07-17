import pandas as pd

def cargar_datos_excel(ruta_archivo=r"base_de_datos.xlsx"):
    """
    Se va a cargar el archivo Excel que contiene las relaciones de préstamos interbancarios.
    Columnas esperadas: 'Banco_Origen', 'Banco_Destino', 'Monto', 'Fecha'.

    Retorna un DataFrame limpio con tipos correctos.
    """
    try:
        df = pd.read_excel(ruta_archivo)
        print("Columnas encontradas:", df.columns.tolist())
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

    columnas_necesarias = ['Banco_Origen', 'Banco_Destino', 'Monto', 'Fecha']
    for col in columnas_necesarias:
        if col not in df.columns:
            print(f"Falta la columna: {col}")
            return None

    df = df.dropna(subset=columnas_necesarias)
    df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce')
    df = df.dropna(subset=['Monto'])
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df = df.dropna(subset=['Fecha'])
    df = df.reset_index(drop=True)
    return df

if __name__ == "__main__":
    ruta = r"base_de_datos.xlsx"
    datos = cargar_datos_excel(ruta)
    if datos is not None:
        print("Primeras filas del archivo cargado:")
        print(datos.head())
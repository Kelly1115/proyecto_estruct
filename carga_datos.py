import pandas as pd
#De prueba
# Lee el archivo Excel
df = pd.read_excel("red_prestamos_interbancarios_unica_hoja (1).xlsx")  # Cambia el nombre por el de tu archivo

df.head(51) # Muestra las primeras filas para analizar la estructura del datasetimport networkx as nx

# Ver columnas y tipos de datos
print(df.columns)
print(df.dtypes)

# Revisar valores nulos
print(df.isnull().sum())

# Verificar si hay duplicados
print(df.duplicated().sum())

# Eliminar duplicados si hay
df = df.drop_duplicates()

# Mostrar valores únicos en columnas clave
print(df['banco_origen'].unique())
print(df['banco_destino'].unique())
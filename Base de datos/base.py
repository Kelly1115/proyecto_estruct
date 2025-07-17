import pandas as pd

# Cargar el archivo Excel subido
file_path = "relaciones_bancarias_ecuador.xlsx"
df = pd.read_excel(file_path)
df.head(6) # Muestra las primeras filas para analizar la estructura del dataset
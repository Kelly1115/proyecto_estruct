import os
import random
import pandas as pd
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from datetime import datetime

os.makedirs('static', exist_ok=True)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def calcular_probabilidad_fraude(fila):
    prob = 10
    if fila['Monto'] > 1500000:
        prob += 10
    if fila['Canal'].lower() == 'online':
        prob += 10
    hora = pd.to_datetime(fila['Hora']).hour
    if 0 <= hora < 5:
        prob += 5
    if fila['Banco_Origen'] == fila['Banco_Destino']:
        prob += 10
    if fila['Internacional'].lower() == 'sí':
        prob += 20
    fecha = pd.to_datetime(fila['Fecha'])
    if fecha.weekday() >= 5:
        prob += 10
    return prob

def asignar_fraude(probabilidad):
    return random.randint(1, 100) <= probabilidad

def generar_graficas(df):
    plt.figure(figsize=(5, 4))
    plt.hist(df['Monto'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Histograma de Montos')
    plt.xlabel('Monto')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.savefig('static/histograma.png')
    plt.close()

    plt.figure(figsize=(5, 4))
    horas = pd.to_datetime(df['Hora']).dt.hour
    plt.scatter(horas, df['Monto'], c='green')
    plt.title('Dispersión: Hora vs Monto')
    plt.xlabel('Hora')
    plt.ylabel('Monto')
    plt.tight_layout()
    plt.savefig('static/dispersion.png')
    plt.close()

    conteo = df['Fraudulenta'].value_counts()
    plt.figure(figsize=(4, 4))
    conteo.plot(kind='bar', color=['orange', 'red'])
    plt.title('Transacciones: Buenas vs Fraudulentas')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/comparativa.png')
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        archivo = request.files['archivo']
        if archivo.filename.endswith('.csv'):
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
            archivo.save(ruta)
            df = pd.read_csv(ruta)
            df['Probabilidad'] = df.apply(calcular_probabilidad_fraude, axis=1)
            df['Fraudulenta'] = df['Probabilidad'].apply(lambda p: 'Sí' if asignar_fraude(p) else 'No')
            generar_graficas(df)
            resumen = df['Fraudulenta'].value_counts().to_dict()
            return render_template('resultado.html', resumen=resumen)
        else:
            return "Por favor sube un archivo .csv válido."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

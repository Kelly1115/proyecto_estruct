from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    datos = [
        {'nombre': 'Juan', 'edad': 20},
        {'nombre': 'Ana', 'edad': 22},
        {'nombre': 'Luis', 'edad': 19}
    ]
    return render_template('index.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)


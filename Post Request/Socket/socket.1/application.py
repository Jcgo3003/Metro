# Aplicacion prueba
from flask import Flask, jsonify, redirect, render_template, request, session

# numero global para actualizar estado
numero = 0

# Configurando la aplicacion
app = Flask(__name__)


# Obteniendo el Post resquest
@app.route('/lec', methods=['GET', 'POST'])
def lec():
    sensor = 0
    if request.method == 'POST':
        ######### Obteniendo datos de los sensores ################
        # Para indentificar el sensor
        sensor = int(request.headers.get('sensor'))
        print('Sensor:', sensor )


    a = request.args.get('a', 0, type=int)
    print('A es ', a)

    global  numero

    numero = sensor + 1
    print('numero es ', numero)

    return jsonify(pro = numero)

# Index/Pantalla principal
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

# Esto NO FUNCIONO
# el resultado no se mantiene ni aunque sea una variable global
# En cuanto jsonify lo toma deja de ser modificable
# eliminando la posibilidad de hacer nada
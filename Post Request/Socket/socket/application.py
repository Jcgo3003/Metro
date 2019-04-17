# Aplicacion prueba
from flask import Flask, jsonify, redirect, render_template, request, session

# Configurando la aplicacion
app = Flask(__name__)

# Obteniendo el Post resquest
@app.route('/nes', methods=['POST'])
def estado():
    if request.method == 'POST':

        # Para indentificar el sensor
        sensor = int(request.headers.get('sensor'))
        print('Sensor:', sensor )

        # enviar dato sensor a otra app
        # Guardar datos en la bd

        ######### Cuando admin envie senal #########
        # 1 Llamar a promedios, rellenar promedios

        # 2 Evaluar y guardar los datos del Estado
        pro = sensor + 3
        print(pro)

        # 3 Presentar esos datos a index en de acuerdo a como se modifiquen
        return jsonify( pro = pro)


# Index/Pantalla principal
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

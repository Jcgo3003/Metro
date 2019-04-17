from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
import time

from helpers import promedios, regis


# Configurando la aplicacion
app = Flask(__name__)


# Ensure templates are auto-reloaded
# app.config["TEMPLATES_AUTO_RELOAD"] = True

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Obteniendo el Post resquest de los Sensores
@app.route('/nes', methods=['POST'])
def api_response():

    if request.method == 'POST':
        ######### Obteniendo datos de los sensores ################
        # Para indentificar dir
        dir = str(request.headers.get('direccion'))
        print('Direccion:', dir )

        # Para indentificar el sensor
        sensor = str(request.headers.get('sen_n'))
        print('Sensor:', sensor )

        # Para indentificar el sensor
        num_sen = int(request.headers.get('num'))
        print('Numero:', num_sen )

        # Llmando a la funcion de registro
        est = regis( dir, sensor, num_sen)
        print(est)

        if est == 'Parfait':
            return 'ok'
        else:
            return(est)

    else:
        return 'Error de submicion de datos'



# Funcion para Entrar a la pagina de admin
@app.route('/control')
def control():
    return render_template('login.html')


# Funcion para redirigir a la pagina de admin/error
@app.route('/login', methods =['GET', 'POST'])
def login():
    """ Login a el admin"""

    if request.method == 'POST':
        # Protegiendo la funcion de los espacios vacios
        if not request.form.get("usuario"):
            return render_template('error.html', msj = "Tienes que poner nombre de usuario")
        elif not request.form.get("password"):
            return render_template('error.html', msj = "Tienes que poner el password")

        # Agregado el usuario y la contrasena
        usuario = request.form.get("usuario")
        contrasena = request.form.get("password")

        # Aqui estan las credenciales
        if usuario != 'admin':
            return render_template('error.html', msj = 'Usuario incorrecto')
        elif contrasena != 'dziewczynka':
            return render_template('error.html', msj = 'Password incorrecto')
        else:
            return render_template("admin.html")


# Aplicacion para leer bd
@app.route('/lec')
def lec():
    """Lee la BD y obtiene los promedios de tiempo """
    a = request.args.get('a', 0, type=str)
    print('La respuesta es ', a)

    if a == "default":
        nombrebd = "default.db"
        print("leyendo bd default")
        # Para leer la bd actual
    else:
        nombrebd = time.strftime('%d%m%y',time.localtime()) + ".db"
        print("leyendo bd actual ", nombrebd)

    pro = promedios(nombrebd)

    return jsonify(pro = pro)


# Aplicacion para obtener los datos desde funcion Nes y de lectura, El estado del Metro
# De esta funcion de encargara celery!!!!!!!!!!!!!! MUY IMPORTANTE
@app.route('/est_met', methods=['POST'])
def est_met():
    return "hacer el programa"

# Index/Pantalla principal
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')









































































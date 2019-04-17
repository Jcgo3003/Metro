# Version Beta 1
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit
import time

from helpers import promedios, regis
from eva import evaluacion, eva_final
from tiempo_past import prom_past

# Configurando flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nadiesabe'

#Llama a socketIO y lo empareja con socket
socket = SocketIO(app, async_mode=None)

# Contando usuarios en linea - Global
num_us = 0
num_us_f = 0

# Variable para mostrar estado - Global
estado_m_a = [0, 0, 0]
estado_m_b = [0, 0, 0]

# Para promedios
prom_a = [0, 0, 0]
prom_b = [0, 0, 0]

# horas esperadas
hora_esp_a = [0, 0, 0]
hora_esp_b = [0, 0, 0]

# Activando funcion evaluacion
activado = 0

# bd
bd = 'nada'

# Color
color_a = 'Sin datos'
color_b = 'Sin datos'

######### Obteniendo datos de los sensores ################
@app.route('/nes',  methods=['GET', 'POST'])
def api_response():
    # Variables globales del programa
    global prom_a
    global prom_b
    global hora_esp_a
    global hora_esp_b
    global estado_m_a
    global estado_m_b
    global activado
    global bd
    global color_a
    global color_b
    # Resgitro en BD
    if request.method == 'POST':
        dir = str(request.headers.get('direccion')) # Para indentificar dir
        print('Direccion:', dir )

        num_sen = int(request.headers.get('num'))  # Para indentificar el sensor
        print('Numero:', num_sen )

        # Llamando a la funcion de registro en BD
        bd_reg = regis( dir, num_sen)
        print('Regis', bd_reg)

        ##### --- Evaluando --- #####
        # Evaluando - cuando 1 es activado y regis accepta los datos
        if (activado == 1 and bd_reg == 'ok'):
            if dir == 'a':
                # restando - 1 al num de sensor para ordenar las cosas
                n_lista = num_sen - 1
                # Obteniendo los datos necesarios
                prom = prom_a[n_lista]
                hora_esp = hora_esp_a[n_lista]

                # Creando hora esperada con prom_past
                if hora_esp  == 0:
                    print('Creando tiempo esperado con bd')
                    hora_esp = prom_past( dir, num_sen, prom, bd )

                # Llamando a Eva
                resultados = evaluacion( prom , hora_esp  )

                # Guardando tiempo esperado proximo
                hora_esp_a[n_lista] = resultados[1]

                # Guardando evaluacion
                estado_m_a[n_lista] = resultados[0]

                # Evaluacion final en base a todos los tiempos
                lista  = estado_m_a
                color_a = eva_final( lista )

                # ENVIAR ESA RESPUESTA AL WEBSOCKET
                socket.emit('update_a', {'estado':color_a }, namespace='/test')

            # Evaluando direccion B
            else:
                # restando - 1 al num de sensor para ordenar las cosas
                n_lista = num_sen - 1
                # Obteniendo los datos necesarios
                prom = prom_b[n_lista]
                hora_esp = hora_esp_b[n_lista]

                # Creando hora esperada con prom_past
                if hora_esp  == 0:
                    print('Creando tiempo esperado con bd')
                    hora_esp = prom_past( dir, num_sen, prom, bd )

                # Llamando a Eva
                resultados = evaluacion( prom , hora_esp  )

                # Guardando tiempo esperado proximo
                hora_esp_b[n_lista] = resultados[1]

                # Resultados obtiene - evaluacion - y - hora esperada
                estado_m_b[n_lista] = resultados[0]

                # Evaluacion final en base a todos los tiempos
                lista  = estado_m_b
                color_b = eva_final( lista )

                # ENVIAR ESA RESPUESTA AL WEBSOCKET
                socket.emit('update_b', {'estado':color_b }, namespace='/test')

        # Respuesta a sensores
        if bd_reg == 'ok':
            return 'Sensor resistered sussesfully'
        else:
            return(bd_reg)

    # === Activando las funciones de evaluacion ===
    elif request.method == 'GET':
        # Respuesta del admin
        a = request.args.get('a', 0, type=str)

        # Decidiendo entre BD
        if a == "default":
            nombrebd = "default.db"
            print("leyendo bd default")
            # Para leer la bd actual
        else:
            nombrebd = time.strftime('%d%m%y',time.localtime()) + ".db"
            print("leyendo bd", nombrebd)

        # Esta bd es la que se utilizara
        bd = nombrebd

        # Obteniendo el promedio segun la decision
        prom_f = promedios(nombrebd)
        prom_a = prom_f[0]
        prom_b = prom_f[1]

        print('a',prom_f[0])
        print('b',prom_f[1])

        # Ajustando var. de activacion
        if prom_f == 'Error!':
            activado = 0
        else:
            activado = 1
            print("MODO EVALUACION")

        # Regresa lista de promedios a la funcion getson de admin
        return jsonify(pro = prom_f)

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

# Index
@app.route('/')
def index():
    return render_template('index.html')

#  --------- Sockets en Accion ---------
# Cuando se conecta un nuevo cliente se ejecutaran las siguientes intrucciones
@socket.on('connect', namespace='/test')
def test_connect():
    # Contando usuarios en linea
    global num_us
    num_us += 1
    # Contando usuarios en linea totales
    global num_us_f
    num_us_f += 1

    print('Numero de usuarios ', num_us)
    print('Client connected')

    # Emitiendo info con el socket a new, con color empaquetado en datos, por /test
    global color_a
    global color_b
    socket.emit('update_a', {'estado':color_a }, namespace='/test')
    socket.emit('update_b', {'estado':color_b }, namespace='/test')

    # numero de usuarios
    socket.emit('num_usu', {'numero':num_us }, namespace='/test')

#  Cuando un cliente se desconecte esto ocurrira
@socket.on('disconnect', namespace='/test')
def test_disconnect():
    global num_us
    num_us -= 1

    # numero de usuarios
    socket.emit('num_usu', {'numero':num_us }, namespace='/test')

    print('Numero de usuarios', num_us)
    print('Client disconnected')

# configuarando el nombre de las apps y la manera en que correra
if __name__ == '__main__':
    socket.run(app, debug=True)

# Esta version contiene los siguientes cambios
# codigo limpio listo para ser ejecutado


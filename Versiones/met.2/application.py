# Primera version Metro - Mezclando admir.4 con Socket.6
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit
import time

from helpers import promedios, regis
from eva import evaluacion, eva_final
from tiempo_past import prom_past

# Configurando flask
app = Flask(__name__)

# Llama a socketIO y lo empareja con socket
# socket = SocketIO(app, async_mode=None)

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
    # Resgitro en BD
    if request.method == 'POST':
        dir = str(request.headers.get('direccion')) # Para indentificar dir
        print('Direccion:', dir )

        sensor = str(request.headers.get('sen_n')) # Para indentificar el sensor

        num_sen = int(request.headers.get('num'))  # Para indentificar el sensor
        print('Numero:', num_sen )

        # Llamando a la funcion de registro en BD
        bd_reg = regis( dir, sensor, num_sen)
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
                final = eva_final( lista)
                print('html ', final)

                # ENVIAR ESA RESPUESTA AL WEBSOCKET

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
                final = eva_final( lista)
                print('html ', final)

                # ENVIAR ESA RESPUESTA AL WEBSOCKET

        # Respuesta a sensores
        if bd_reg == 'ok':
            return 'Sensor resistered sussesfully'
        else:
            return(bd_reg)

    # === Activando las funciones de evaluacion ===
    elif request.method == 'GET':
        # Respuesta del admin
        a = request.args.get('a', 0, type=str)
        print('La respuesta es ', a)

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

if __name__ == '__main__':
    app.run(debug=True)
    # socket.run(app, debug=1)

# Esta version contiene los siguientes cambios
#
# Modificare eva
# Agregare funcion prom_pas
# esta funcion se encargara de evaluar directamente el tiempo leyendo los datos de
# La Bd - Pero solo cuando hora_esp_' '
#
# Funcion prom_pas
# Recibira dos 3 variables
# Direccion, sensor, promedio, bd
# recibiendo esto leera la bd
# leera las rondas
# Justo cuando reciba el sensor 1 leera ese sensor pero su entrada anterior
# Cuando obtenga ese tiempo
# Creara un tiempo esperado a partir de el y eso segura adelante
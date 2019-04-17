# Primera version Metro - Mezclando admir.4 con Socket.6
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit
import time

from helpers import promedios, regis
from eva import evaluacion, eva_final

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
    # Resgitro en BD
    if request.method == 'POST':
        dir = str(request.headers.get('direccion')) # Para indentificar dir
        print('Direccion:', dir )

        sensor = str(request.headers.get('sen_n')) # Para indentificar el sensor
        print('Sensor:', sensor )

        num_sen = int(request.headers.get('num'))  # Para indentificar el sensor
        print('Numero:', num_sen )

        # Llamando a la funcion de registro en BD
        bd_reg = regis( dir, sensor, num_sen)
        print(bd_reg)

        # Evaluando - cuando 1 es activado y regis accepta los datos
        if (activado == 1 and bd_reg == 'ok'):
            if dir == 'a':
                # restando - 1 al num de sensor para ordenar las cosas
                nnum_sen -= 1
                # Obteniendo los datos necesarios
                prom = prom_a[num_sen]
                hora_esp = hora_esp_a[num_sen]

                # Llamando a Eva
                resultados = evaluacion( prom , hora_esp  )

                # Guardando tiempo esperado proximo
                hora_esp_a[num_sen] = resultados[1]

                # Guardando evaluacion
                estado_m_a[num_sen] = resultados[0]

                # Evaluacion final en base a todos los tiempos
                lista  = estado_m_a
                final = eva_final( lista)
                print('estado final para a es', final)

                # ENVIAR ESA RESPUESTA AL WEBSOCKET


            # Evaluando direccion B
            else:
                # restando - 1 al num de sensor para ordenar las cosas
                num_sen -= 1
                # Obteniendo los datos necesarios
                prom = prom_b[num_sen]
                hora_esp = hora_esp_b[num_sen]

                # Llamando a Eva
                resultados = evaluacion( prom , hora_esp  )

                # Guardando tiempo esperado proximo
                hora_esp_b[num_sen] = resultados[1]

                # Resultados obtiene - evaluacion - y - hora esperada
                estado_m_b = resultados[0]

                # Evaluacion final en base a todos los tiempos
                lista  = estado_m_a
                final = eva_final( lista)
                print('estado final para b es', final)

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
            print("leyendo bd actual ", nombrebd)

        # Obteniendo el promedio segun la decision
        prom_f = promedios(nombrebd)
        prom_a = prom_f[0]
        prom_b = prom_f[1]

        print('a',prom_f[0])
        print('b',prom_f[1])

        # Ajustando var. de activacion
        # global activado
        activado = 1

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

# La parte que evaluara los sensores esta protegida por medio del seguro que tiene regis
#      El seguro que tiene 'BD regis' sirve para evitar errores de lectura cuando un sensor se despara cuando no se espera
#      Como desventaja cuando un sensor no se dispare, se perderan los registros a partir de ese sensor
#           Al no ser activado el sensor, el programa no registrara ese movimiento y a partir de ahi no registrara ningun movimiento
#
# Por otra parte el programa de evaluacion no require de ese seguro?, por que a evaluacion solo le interesan los tiempos
# Si lo require porque si se activa un sensor por error ocacionara un error de lectura y evaluara incorrectamente
#       Como crear un seguro que pueda diferenciar entre senal por error y una correcta
#           Tipos de senal de error
#           Cuando un sensor arroja una senal, que se active solo
#               Para arreglar ese error, fue implementar un seguro que en base a las rondas decide que esa senal no se espera
#               Por lo que no la registra, la ignora por completo
#           Cuando un sensor no registra una senal
#               No he implementado nada para este tipo de error, de vez en cuando pasa que los sensores no son activados
#               No detectan el movimiento y no envian ninguna senal
#                   Cuando eso pasa mas el seguro de arriva se producce algo un mega error, haciendo que las senales reales
#                   No se registren por culpa de ese sensor, como podriamos saber que un sensor fallo?
#                   Agragando un doble sensor o algo asi
#       Para efectos de lo pequeno que es el proyecto, seguiremos con el seguro de arriva, pero le agregare un
#           Tercer seguro - si las rondas estan 1,0,0 y se recibe una senal del primer sensor, quiere decir que toda
#               Esa lectura fallo, un sensor no dio lectura e hizo que la funcion seguro no registrara esa vuelta
#                           Para solucionar eso, si el sensor 1 tiene mas de 2, se borrara la linea donde se dejo de registrar
#                           Donde se produjo el fallo, se borrar la ronda nueva y se anadira el nuevo registro sobre lo borrado
#
# Confiaremos en regis en cuanto el resguardo de los errores    por lo que
# evaluacion solo funcionara cuando bd regis accepte los datos
#
# Sockets segunda revision - Sockets
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Configurando flask
app = Flask(__name__)

# Llama a socketIO y lo empareja con socket
socket = SocketIO(app, async_mode=None)

# Contando usuarios en linea - Global
num_us = 0
num_us_f = 0

# Variable para mostrar estado - Global
color = 'Sin datos'

# Ruta para obtener info via POST request
@app.route('/read', methods=['POST'])
def read():
    # Obteniendo datos via POST
    if request.method == 'POST':
        info = int(request.headers.get('info'))

        # Prosesando los datoss
        global color
        if info == 0:
            color = "No color"
        elif ( info > 0 and info < 100 ):
            color = "red"
        elif ( info >= 100 ):
            color = "blue"
        else:
            color = "Unknow"
        print(color)

        # Emitiendo info con el socket a new, con color empaquetado en datos, por /test
        socket.emit('update', {'estado':color }, namespace='/test')
        return 'ok'

    else:
        return "Error de envio"

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
    global color
    socket.emit('update', {'estado':color }, namespace='/test')

#  Cuando un cliente se desconecte esto ocurrira
@socket.on('disconnect', namespace='/test')
def test_disconnect():
    global num_us
    num_us -= 1

    print('Numero de usuarios', num_us)
    print('Client disconnected')

# configuarando el nombre de las apps y la manera en que correra
if __name__ == '__main__':
    socket.run(app, debug=True)

# Probablemente para efectos de prueba seria muy comodo
# Tener dos versiones para envio de datos para poder cambiar a mi antojo
# Veo que los sockets estan tardando algunos varios segudos en activarse y eso me preocupa
# Desarrollar las dos opciones
# Sockets y Long-pulling
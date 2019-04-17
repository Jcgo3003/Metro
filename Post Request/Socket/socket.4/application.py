# Version que implementa satisfactoriamente los sockets en lugar del long-pulling request
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

# Configurando flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# Llama a socketIO y lo empareja con con_s
async_mode = None
con_s = SocketIO(app, async_mode=async_mode)

# Contando los usuarios en linea
n_usuarios = 0
n_usuarios_f = 0

# Global variable that needs to keep updated
var_g = 0

# Getting the post resquest
@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'POST':
        # Getting the data to update from headers of post request
        info = int(request.headers.get('info'))
        print(info)

        # Trying to keep the changes with a global variable
        global var_g
        var_g = info

    print(var_g)
    # Procesing data
    if var_g == 0:
        color = "No color"
    elif ( var_g > 0 and var_g < 100 ):
        color = "red"
    elif ( var_g >= 100 ):
        color = "blue"
    else:
        color = "Unknow"
    print(color)

    # Emitiendo info con ayuda del socket
    con_s.emit('new', {'datos':color }, namespace='/test')
    return 'ok'

# Index
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', async_mode=con_s.async_mode)

# Cuando se conecta un nuevo cliente se ejecutaran las siguientes intrucciones
@con_s.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    # global hilo
    global n_usuarios
    n_usuarios += 1
    global n_usuarios_f
    n_usuarios_f += 1
    print('Numero de usuarios ', n_usuarios)
    print('Client connected')


#  Cuando un cliente se desconecte esto ocurrira
@con_s.on('disconnect', namespace='/test')
def test_disconnect():
    global n_usuarios
    n_usuarios -= 1
    print('Numero de usuarios', n_usuarios)
    print('Client disconnected')

# configuarando el nombre de las apps y la manera en que correra
if __name__ == '__main__':
    con_s.run(app, debug=True)
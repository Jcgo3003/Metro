from flask import Flask, jsonify, render_template, request

# Global variable that needs to keep updated
var_g = 0

app = Flask(__name__)

# Getting the post resquest
@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'POST':
        # Getting the data to update from headers of post request
        info = int(request.headers.get('info'))

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

    return jsonify(color = color)

# Index
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
# Por fin logre que esta aplicacion se actualice como debe ser
# Ahora funcion read para llevarse al siguiente plano debe...
#  1 Leer y guardar en db los datos
#  2 cuando le diga empezar desde la admin que empieze, si no que solo registre los
#           movimientos en la bd
#  3
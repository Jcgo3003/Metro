from flask import Flask, request, Response, redirect, render_template, session, url_for

import time

num_reg = 0

app = Flask(__name__)

# obteniendo el post resquest
@app.route('/api', methods=['POST'])
def api_response():
    #antes guarda el valor de cuando comenzo a correr el while
    antes = time.perf_counter()


    if request.method == 'POST':
        #despues es el valor del tiempo despues de recibir respuesta
        despues = time.perf_counter()

        # Actualizando el registro
        num_reg += 1

        #calculando el tiempo para saver cuanto tiempo paso
        t_sensor1 = despues - antes
        print()
        print("Tiempo %",t_sensor1)
        print("Numero de registro %" ,num_reg)

    # Output comparison
    return "ok"

@app.route("/")
def index():

    return render_template("index.html")
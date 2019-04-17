from flask import Flask, render_template
import time

app = Flask(__name__)


@app.route("/")
def template_test():
    num_reg = 0
    hora_reg = 0
    tiempo_d_reg = 0
    #tiempo_f = 0

    # sensor contando el tiempo
    sensor1 = input("Comenzar el programa ")
    tiempo_i = time.asctime(time.localtime(time.time()))
    while( sensor1 != 0):
        antes = time.perf_counter()
        sensor1 = int(input("Esperando respuesta: "))
        despues = time.perf_counter()

        # Actualizando el registro
        num_reg += 1

        #tiempos capturados
        print('antes ', antes)
        print('despues', despues)

        #calculando el tiempo
        t_sensor1 = despues - antes
        print(t_sensor1)
    # Obteniedo el tiempo final
    tiempo_f = time.asctime(time.localtime(time.time()))

    # Imprimiendo los parametros
    print()
    print('Tiempo inicial', tiempo_i)
    print('Numero de registros ', num_reg)
    print('Tiempo final ', tiempo_f)
    return render_template('template.html', my_string="t_sensor1")


if __name__ == '__main__':
    app.run(debug=True)
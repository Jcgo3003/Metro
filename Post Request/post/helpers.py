import time

def metro( a ):
    # # Obteniendo el valor para el numero de sensores
    # num_sen = input("Introduce numero de sensores ")

    # # Obteniendo el valor para el numero de registros
    # num_res = input("Introduce numero de registros para el 'Modo programacion' ")

    # Escribir la parte del programa que confirmara que los sensores estan en linea

    # Declarando las variables - tengo que hacer una clase con estos registros
    #tiempo_i = 0
    num_reg = 0
    hora_reg = 0
    tiempo_d_reg = 0

    # sensor contando el tiempo
    sensor1 = a
    # cuenta el tiempo desde que comenzo a recibir un post
    tiempo_i = time.asctime(time.localtime(time.time()))

    #el programa funcionara hasta que metro reciba 0
    while( sensor1 != 0):
        #antes guarda el valor de cuando comenzo a correr el while
        antes = time.perf_counter()
        sensor1 = a
        #despues es el valor del tiempo despues de recibir respuesta
        despues = time.perf_counter()

        # Actualizando el registro
        num_reg += 1

        #calculando el tiempo para saver cuanto tiempo paso
        t_sensor1 = despues - antes
        return t_sensor1
    # Obteniedo el tiempo final
    # tiempo_f = time.asctime(time.localtime(time.time()))
    # return tiempo_f

import time

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


##Primeros avances implementacion del cronometro 19 - 03
# Agregue las fechas de inicio y termino 20- 30
# Debo agregra la posibilidad de guardar todo eso en un cvs
# Necesito hacer que el programa vaya guardando sus resgistros para poder en un tupple o lista no lo se
# Elegir sus mejores tiempos
# Agragar hora e intertar agregar una manera para que los guarde, tal vez hacer una clase para
# para contener los datos sobre los sensores y los cvs para que los vaya registrando
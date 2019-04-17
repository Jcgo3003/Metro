import time
from datetime import datetime, timedelta
import datetime as dt

# valores para delta time
FMT = '%H:%M:%S'

def evaluacion( prom, hora_esp):
    # Introduciendo datos al programa
    prom = prom
    hora_esp = hora_esp

    # Hora Now
    t_now = dt.datetime.now()

    # Conversion de TIEMPO ESPERADO a formato STR de nuevo para que pueda ser evaluado
    t_esp_str = hora_esp.strftime('%H:%M:%S')
    t_now_str = t_now.strftime('%H:%M:%S')

    # Resta - PARA EVA
    tdel = datetime.strptime(t_now_str, FMT) - datetime.strptime(t_esp_str, FMT)
    tdel_int = int(round(tdel.total_seconds()))

    # crear TIEMPO ESPERADO - Conversion a tiempo en h,m,s en datetime formato
    #Tiempo promedio en segundos
    t_pro_s = int(prom)
    # Conversion a tiempo en h,m,s en datetime formato
    t_pro_f = dt.timedelta(seconds = t_pro_s)

    # Nuevo tiempo esperado
    t_esp_nuevo = t_now + t_pro_f


####### Evaluando el tiempo esperado
    eva = 0
    print('tiempo a evaluar', tdel_int)
    if ( tdel_int < 0) :
        eva = 1 # Super buen servicio

    elif( tdel_int >= 0 and tdel_int < 9):
        eva = 2 # servicio ok

    elif( tdel_int >= 9 and tdel_int < 18):
        eva = 3 # Servicio mas o menos

    elif( tdel_int >=18  and tdel_int < 27):
        eva = 4 # Servicio malo

    elif( tdel_int >=27 and tdel_int < 36 ):
        eva = 5 # Servicio muy malo
    else:
        eva = 6 # servicio fuera de lo esperado!!!!!!!!!

    # regresando evaluacion , regresando tiempo esperado
    print('La evaluacion eva es', eva)
    print('tiempo esperado', t_esp_nuevo)
    return( eva, t_esp_nuevo)


def eva_final( lista ):
    lista = lista
    long_real = 0
    suma = 0
    print('Evaluacion',lista)
    for i in lista:
        if (i != 0 and i != 6 ):
            long_real += 1
            suma += i

    if (suma == 0):
        final = 6
    else:
        final = round(suma/long_real)

    print('Evaluacion final', final)
    return(final)

# Esta version de eva ya solo evaluara y no creara un tiempo esperado a partir de promedio
# Para hacerm as rapida la obtencion de datos se modifico eva final
#   De esta manera despues de la primera vuelta ya se notaran los cambios en el servicio

# Numeros para entender evaluacion
# 1 Super buen servicio
# 2 Servicio ok
# 3 Servicio mas o menos
# 4 Servcico malo
# 5 Servicio muy malo
# 6 Procesando datos
# 0 Sin datos -  Aun no se inicia el programa - Este numero jamas se desplegara
# una vez que este iniciado el programa de evaluacion se comenzara a rellenar la lista
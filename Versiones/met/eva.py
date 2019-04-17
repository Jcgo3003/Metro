import time
from datetime import datetime, timedelta
import datetime as dt

# valores para delta time
FMT = '%H:%M:%S'

def evaluacion( prom, hora_esp):
    # Introduciendo datos al programa
    prom = prom
    hora_esp = hora_esp

    # Si aun  no exite hora_esp, significa que es la primera vez que se inicia este programa
    if hora_esp == 0:
        print('Creando hora esperada')
        #Tiempo promedio en segundos
        t_pro_s = int(prom)

        # Conversion a tiempo en h,m,s en datetime formato
        t_pro_f = dt.timedelta(seconds = t_pro_s)

        # Introduccion de tiempo NOW en datetime
        t_now = dt.datetime.now()

        # Suma de esos tiempos para crear TIEMPO ESPERADO
        t_esp = t_now + t_pro_f
        print(t_esp)

        # Evaluacion final
        eva = 6

        print('Primer registro ')
        return( eva, t_esp)

    # Si ya hay hora esperada directamente evalua su desempeno
    else:
        print('desempeno')
        # Hora Now
        t_now = dt.datetime.now()
        print('La hora now es', t_now)
        # Conversion de TIEMPO ESPERADO a formato STR de nuevo para que pueda ser evaluado
        t_esp = hora_esp
        print('La hora esp recibida es', t_esp)
        t_esp_str = t_esp.strftime('%H:%M:%S')
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
        if ( tdel_int < 0) :
            eva = 1 # Super buen servicio

        elif( tdel_int >= 0 and tdel_int < 4):
            eva = 2 # servicio ok

        elif( tdel_int >= 4 and tdel_int < 8):
            eva = 3 # Servicio mas o menos

        elif( tdel_int >= 8 and tdel_int < 12):
            eva = 4 # Servicio malo

        elif( tdel_int >=12 and tdel_int < 16):
            eva = 5 # Servicio muy malo

        # regresando evaluacion , regresando tiempo esperado
        print('La evaluacion es', eva)
        print('tiempo esperado', t_esp_nuevo)
        return( eva, t_esp_nuevo)


def eva_final( lista ):
    lista = lista

    long_real = 0
    suma = 0
    for i in lista:
        if i != 0:
            long_real += 1
            suma += i

    final = round(suma/long_real)
    return(final)

# Eva es una funcion que evalua un tiempo contra otro
# Recibe datos de promedio y tiempo esperado
# Dependiendo cual de los dos reciba sera la evalucion
#   Si solo recibe tiempo promedio no hara ninguna evalaucion - solo dira que ya esta trabajando en ello
#   Si recibe un tiempo esperado hara una evaluacion del tiempo esperando contra el actual
#       De manera que evaluara si el tiempo que paso contra el tiempo esperado
#   El resultado de esta evalaucion lo regresa, y tambien regresa un tiempo esperado en todas la ocaciones

# Numeros para entender evaluacion
# 1 Super buen servicio
# 2 Servicio ok
# 3 Servicio mas o menos
# 4 Servcico malo
# 5 Servicio muy malo
# 6 Procesando datos
# 1000 Servico caido - NO en este programa
# El numero 182 significa que ya esta procesado un tiempo en espera
# 0 Sin datos -  Aun no se inicia el programa - Este numero jamas se desplegara
# una vez que este iniciado el programa de evaluacion se comenzara a rellenar la lista
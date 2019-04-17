# Librerias
import sqlite3
import time
import os.path
from datetime import datetime, timedelta


# ------------------------------------------------------ #
################ Lectura de bd y promedios ###############
# ------------------------------------------------------ #
def promedios(nombrebd):

    # Nombre para la BD recibido
    nombrebd = nombrebd

    # Numero de rondas registradas en la BD
    ron_a = [ 0 , 0 , 0 ]
    ron_b = [ 0 , 0 , 0 ]

    # --------------------------------------------------------------------- #
    ################ Comienzo - Creando/Leyendo archivo de BD ###############
    # --------------------------------------------------------------------- #
    if (os.path.isfile(nombrebd)):
        # Conectando la BD
        conexion = sqlite3.connect(nombrebd)

        # Cursor
        c = conexion.cursor()

        ### Recuperando datos de la DB direccion A #####
        # sen1 - selecciona la columna sen1_a - asigna bd toda esa columna que se guarda como lista - asigna el # de longitud de esa lista
        c.execute("SELECT sen1_a FROM a")
        bd = c.fetchall()
        ron_a[0] = len(bd)

        # sen2 - hace los mismo para la columna de sen2 con algunas diferencias para eliminar las entradas con 'NONE'
        c.execute("SELECT sen2_a FROM a")
        bd = c.fetchall()
        # filtrando las entradas para quitar "NONE" de la lista de entradas
        cuenta = 0
        for i in range (len(bd)):
            if ( str(bd[i][0]) != 'None'):
                cuenta += 1
        # asigna cuenta a ron_a[1]
        ron_a[1] = cuenta

        # sen3 - Utiliza el mismo metodo para contar en esta columna
        c.execute("SELECT sen3_a FROM a")
        bd = c.fetchall()
        cuenta = 0
        for i in range (len(bd)):
            if ( str(bd[i][0]) != 'None'):
                cuenta += 1
        ron_a[2] = cuenta

        ### Recuperando datos de la DB  para la vuelta  direccion B ##### Hace exactamente lo mismo pero para las columnas en B
        # sen3
        c.execute("SELECT sen3_b FROM b")
        bd = c.fetchall()
        ron_b[2] = len(bd)

        # sen2
        c.execute("SELECT sen2_b FROM b")
        bd = c.fetchall()
        cuenta = 0
        for i in range (len(bd)):
            if ( str(bd[i][0]) != 'None'):
                cuenta += 1
        ron_b[1] = cuenta

        # sen1
        c.execute("SELECT sen1_b FROM b")
        bd = c.fetchall()
        cuenta = 0
        for i in range (len(bd)):
            if ( str(bd[i][0]) != 'None'):
                cuenta += 1
        ron_b[0] = cuenta
        # En este punto ya tenemos las listas de rondas con la cuenta exacta de la ultima entrada
        # De esta manera se reanundan los registros en donde se quedaron
    else:
        #!!!!! MENSAJE DE ERROR !!!!!!!!!!!!
        return("No exite este archivo", nombrebd)

    #-----------------------------------------------------------#
    ############ Promedios de los tiempos por columna ###########
    #-----------------------------------------------------------#
    # Limitando numero de muestra a la ultima linea registrada totalmente / ron_a[2] por que es el ultimo en recibir senal, inicio sera dado por el
    # si hubo mas de 5 vueltas, guarda en ini_a el numero de la linea final - 4 lugares
    if (ron_a[2] > 5):
        ini_a = ron_a[2] - 4
    # si no hubo rondas en absoluto
    elif (ron_a[2] == 0):
        ini_a = 0
    else:
        # si no hubo mas de 5 vueltas comienza desde el registro 1
        ini_a = 1

    # Mismo proceso para dir. 'b'
    if (ron_b[0] > 5):
        # si hubo mas de 5 vueltas/ - 4 para que sea un muestra de 5
        ini_b = ron_b[0] - 4
    # si no hubo rondas en absoluto
    elif (ron_b[0] == 0):
        ini_b = 0
    else:
        ini_b = 1

    # Lista de sensores con sus nombres para iterar con ellos
    l_sen_a = [ 'sen1_a', 'sen2_a', 'sen3_a']
    l_sen_b = [ 'sen1_b', 'sen2_b', 'sen3_b']

    # lista_col guardara los tiempos obtenidos de una columna en particular
    lista_col = []

    # lista de tiempos despues de la sustracion t2 - t1, t3 - t2 , etc.
    lista_t = []

    #promedios
    pro_a = []
    pro_b = []

    # valores para delta time, hora, minuto, segundos
    FMT = '%H:%M:%S'

    # protegiendo en caso de que no haya registros suficientes
    if (ini_a > 1):
        ### !!!!!!!! MENSAJE DE ERROR
        return('No hay rondas para calcular en Dir a ')
    else:
        ### iterando sobre sensores ###
        # Direccion a
        # Para n en un rango de longitun de la lista de sensoresl_sen_a
        for n in range (len(l_sen_a)):

            # Leyendo la ultima fila en columna l_sen_a [ n ]
            # para i en un rango de (inicia en el valor de ini_a), ( y termina en el numero de ronda del ultimo sensor mas 1 ) - mas 1 por que los for terminan en un numero antes del limite, es decir si pongo 11 terminara en 10
            for i in range ( ini_a ,ron_a[2] +1 ):
                # Seleciona la columna del sensor utilizando a n para obtener de l_sen_a el nombre de la columna, e i para el numero de linea del a bd
                c.execute('SELECT {} FROM a WHERE num_a = ?'.format( l_sen_a[n]), ( i , ))
                # Guarda en bd todos los datos de esa columna
                bd = c.fetchone()
                # A lista_col agrega el valor obtenido de esa linea y esa columna en particular, b[0] porque bd es una lista
                lista_col.append( bd[0] )

            # sacando promedio de la lista - menos 1 porque se haran los promedios entre los tiempos de una columna, si son 10 datos seran 9 restas
            for y in range (len(lista_col) -1):
                # Obteniendo la sustracion-resta de t2 - t1 para cada valor de lista_col
                tdel = datetime.strptime(lista_col[y+1], FMT) - datetime.strptime(lista_col[y], FMT)
                # Guardando el valor en segundos
                t_float = tdel.total_seconds()
                # Guardando el valor en la lista_t
                lista_t.append( t_float )

            # guardando el promedio de cada columna en la lista de promedios
            pro_a.append( sum(lista_t)/ len(lista_t) )

            #borrando la listas para que este vacias para la proxima columna y sus datos
            lista_col.clear()
            lista_t.clear()

        # Imprime la lista con los valor promedio que cada columna tiene
        #### DATOS FINALES !!!!!!!!
        print('Promedios finales pro_a',pro_a)

    # protegiendo en caso de que no haya registros b
    if (ini_b > 1):
        ### !!!!!! Mensaje de error
        return('No hay rondas para calcular en Dir b ')
    else:
        ### Direccion b - Mismo metodo pero esta vez aplicado a la linea 'b'
        for n in range (len(l_sen_b)):

            # Leyendo la ultima fila en columna l_sen_a [ n ]
            for i in range ( ini_b ,ron_b[0] +1 ):
                # leyendo las columnas en el mismo orden que con 'a'
                c.execute('SELECT {} FROM b WHERE num_b = ?'.format( l_sen_b[n]), ( i , ))
                # guardando esa consulta en bd
                bd = c.fetchone()
                # agregando esa colsuta a la lista de consultas
                lista_col.append( bd[0] )

            # sacando promedio de la lista
            for y in range (len(lista_col) -1):
                # Obteniendo la sustracion de t2 - t1 para cada valor en lista_col
                tdel = datetime.strptime(lista_col[y+1], FMT) - datetime.strptime(lista_col[y], FMT)
                # Guardando el valor en segundos
                t_float = tdel.total_seconds()
                # Guardando el valor en la lista_t
                lista_t.append( t_float )

            # obteniedo el promedio de esa columna y agragandolo a la lista  de promedios
            pro_b.append( sum(lista_t)/ len(lista_t) )

            #borrando la listas para los siguientes datos
            lista_col.clear()
            lista_t.clear()


        #### resulatdos finales!!!!!
        print('Promedios finales pro_b',pro_b)

    #### Devolviendo los resultados finales como listas
    return(pro_a , pro_b )
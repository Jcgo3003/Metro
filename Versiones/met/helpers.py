# Librerias
import sqlite3
import time
import os.path
from datetime import datetime, timedelta

############################ Lectura de bd y promedios ########################
def promedios(nombrebd):
    # Nombre para la BD recibido
    nombrebd = nombrebd

    # Numero de rondas registradas en la BD
    ron_a = [ 0 , 0 , 0 ]
    ron_b = [ 0 , 0 , 0 ]

    ################ Comienzo - Creando/Leyendo archivo de BD ###############
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
        print("No exite este archivo", nombrebd)
        return 'Error!'
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
    if (ini_a < 1): ###ERROR
        ### !!!!!!!! MENSAJE DE ERROR
        print('No hay rondas para calcular en Dir b ')
        return 'Error!'
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

            # guardando el promedio de cada columna en la lista de promedios REDONDEADOS
            pro_a.append( round(sum(lista_t)/ len(lista_t)) )

            #borrando la listas para que este vacias para la proxima columna y sus datos
            lista_col.clear()
            lista_t.clear()

        # Imprime la lista con los valor promedio que cada columna tiene
        #### DATOS FINALES !!!!!!!! print-----print-print-----print-print-----print-print-----print-
        # print('Promedios finales pro_a',pro_a)

    # protegiendo en caso de que no haya registros b
    if (ini_b < 1):###ERROR
        ### !!!!!! Mensaje de error
        print('No hay rondas para calcular en Dir b ')
        return 'Error!'
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

            # obteniedo el promedio de esa columna y agragandolo a la lista  de promedios REDONDEADOS
            pro_b.append( round(sum(lista_t)/ len(lista_t)) )

            #borrando la listas para los siguientes datos
            lista_col.clear()
            lista_t.clear()


        #### resulatdos finales!!!!! print-----print-print-----print-print-----print-print-----print-
        # print('Promedios finales pro_b',pro_b)

    #### Devolviendo los resultados finales como listas!!!!!!!!!!!!!!!!!!!!!!!!!!
    return(pro_a, pro_b)

############################# REGISTRO DE DATOS EN LA BD ##########################
def regis(dir, sensor, num_sen):
    # obteniendo datos
    dir = dir
    sensor = sensor
    num_sen = num_sen

    # Creando nombre para la BD apartir de la fecha
    nombrebd = time.strftime('%d%m%y',time.localtime()) + ".db"

    # Lista que se encarga de contar el numero de rondas registradas en la BD
    ron_a = [ 0 , 0 , 0 ]
    ron_b = [ 0 , 0 , 0 ]

    ################ Comienzo - Creando/Leyendo archivo de BD ###############
    # Si ya existe el archivo
    if (os.path.isfile(nombrebd)):
        #print("BD existente") print-print-print-print-print-print-print

        # Conectando la BD
        conexion = sqlite3.connect(nombrebd)
        #print ("Leyendo BD: ", nombrebd) print-print-print-print-print-print-print

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

    # Creando la BD nueva
    else:
        # En caso de que no exista la base de datos crea una completamente vacia
        # print("Creando BD ...")print-print-print-print-print-print-print
        # Creando BD
        conexion = sqlite3.connect(nombrebd)
        # print ("Base de datos creada: ", nombrebd) print-print-print-print-print-print-print

        # Cursor para la bd
        c = conexion.cursor()

        # creando tablas
        # Crea tabla 'a' con 'num_a' - registro de rondas, Sen1_a - hora de registro, Sen2_a - hora de registro, Sen3_a - hora de registro.
        c.execute(''' CREATE TABLE "a" ('num_a' INTEGER PRIMARY KEY , 'sen1_a' TIME, 'sen2_a' TIME, 'sen3_a' TIME )''')
        # Crea tabla 'b' con 'num_b' - registro de rondas, Sen1_b - hora de registro, Sen2_b - hora de registro, Sen3_b - hora de registro.
        c.execute(''' CREATE TABLE "b" ('num_b' INTEGER PRIMARY KEY , 'sen3_b' TIME, 'sen2_b' TIME, 'sen1_b' TIME )''')

    # print-----print-print-----print-print-----print-print-----print-
    # print('Las rondas comienzan asi A', ron_a) print-----print-print-----print-print-----print-print-----print-
    # print('Las rondas comienzan asi B', ron_b) print-----print-print-----print-print-----print-print-----print-

    ################ Introduccion de datos a la DB# #########################
    # Seccion para insertar los datos en la bd 'a' ...
    if ( dir == 'a'):
        # Crendo un nueva linea en la BD, por ser el sensor 1 se crea una nueva linea en la bd
        if (num_sen == 1 ):
            # sumando +1 al contador de rondas
            ron_a[0] += 1

            # Asegurando que el registro sea un registro 'esperado' y no un error de lectura - SEGURO 3
            if (ron_a[0] >= (ron_a[1] + 2)):
                # Quitando el +1 que se agrego arriva
                ron_a[0] -= 1

                # borrando el registro donde se produjo el error de no registro por falta de lectura
                c.execute('''DELETE FROM a WHERE num_a = {}'''.format( ron_a[0]) )

                # Registrando este sensor en lugar del otro
                hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                # introduciendo el # de ronda en 'num_a', en la en columna sen1_a, en las demas 'NONE'
                c.execute('''INSERT INTO a ("num_a","sen1_a","sen2_a","sen3_a") VALUES ( ? , ? ,NULL,NULL)''', (ron_a[0], hora_now) )

                # BUSCAR MANERA DE GUARDAR REGISTRO DE ESTOS ERRORES
                print('Error S3 A, falla en resgisto, borrando registro anterior y registrando nuevo')

                # Error!
                conexion.commit()
                conexion.close()
                return 'ok'

            else:
                print("Guardando registro a Dir a, sen%s_a" % (num_sen))

                # obteniendo la hora exacta de ese momento para guardarla en hora_now
                hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                # introduciendo el # de ronda en 'num_a', en la en columna sen1_a, en las demas 'NONE'
                c.execute('''INSERT INTO a ("num_a","sen1_a","sen2_a","sen3_a") VALUES ( ? , ? ,NULL,NULL)''', (ron_a[0], hora_now) )

        # Otros sensores
        else:
            # se resta 1 la numero del sensor para hace que corresponda con numero de sitio de la lista de rondas
            num_sen -= 1
            ron_a[num_sen] += 1

            # protegiendo la lista
            if ((ron_a[num_sen] > ron_a[num_sen-1])):

                # print("Error no se puede agregar registro a Dir a, sen%s_a no se espera a registrar en este momento" % (num_sen+1))
                # Se le quita un numero a la ronda que ya habia guardado y no se guarda nada
                ron_a[num_sen] -= 1

                # Error!!!
                return("Error no se puede agregar registro a Dir a, sen%s_a no se espera a registrar en este momento" % (num_sen+1))

            else:

                # Se obtiene la hora actual y se guarda en hora_now
                hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                # Actualiza los datos, donde estaba 'NONE' ahora estara el valor de hora_now
                # Utiliza sensor - columna, hora_now para el registro, ron_a[num_sen] para colocarlo en la linea correcta
                c.execute('''UPDATE a SET {} = ? where num_a = ? '''.format( sensor), (hora_now, ron_a[num_sen] ) )

    # Seccion para insertar los datos en la bd 'b' ...
    else:
        # Se utiliza el mismo metodo diferente orden al ser el sensor 3 el que empieza, porque el sensor estara
        # Colocado en la ultima estacion de dir. 'a', haciendo que sensor 3 sea la primera en activarse y crea la linea
        if (num_sen == 3 ):

            # Agrega +1 a su cuenta de rondas de nuevo al ser sen3 el primero de dir. 'b' la lista se actulizara de derecha a izquierda
            ron_b[2] += 1

            # Asegurando que el registro sea un registro 'esperado' y no un error de lectura - SEGURO 3
            if ( ron_b[2] >= ( ron_b[1] + 2) ):
                # Quitando el +1 que se agrego arriva
                ron_b[2] -= 1

                # borrando el registro donde se produjo el error de no registro por falta de lectura
                c.execute('''DELETE FROM b WHERE num_b = {}'''.format( ron_b[2]) )

                # Regristrando este sensor en lugar del otro
                hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                c.execute('''INSERT INTO b ("num_b","sen3_b","sen2_b","sen1_b") VALUES ( ? , ? ,NULL,NULL)''', (ron_b[2], hora_now) )

                # BUSCAR MANERA DE GUARDAR REGISTRO DE ESTOS ERRORES
                print('Error s3b, borrando registro anterior y registrando nuevo')

                # Error!
                conexion.commit()
                conexion.close()
                return 'ok'

            else:
                # obteniendo la hora actual y guardandola en hora_now
                hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                # Creando la nueva linea
                c.execute('''INSERT INTO b ("num_b","sen3_b","sen2_b","sen1_b") VALUES ( ? , ? ,NULL,NULL)''', (ron_b[2], hora_now) )

        # Otros sensores en 'b'
        else:
            # Al igual que en 'a' aqui actualizara los datos de esas columnas pasando los 'NONE's a registros de tiempo
            # para que las rondas se guarden correctamente
            num_sen -= 1

            # Sumando +1 a la lista de rondas 'b'
            ron_b[num_sen] += 1

            # protegiendo la lista
            if ((ron_b[num_sen] > ron_b[num_sen+1])):
                # print("Error no se puede agregar registro a Dir b, sen%s_b no se espera a registrar en este momento" % (num_sen+1))
                # Se le quita un numero a la ronda que ya habia guardado y no se guarda nada
                ron_b[num_sen] -= 1
                # Error!
                return("Error no se puede agregar registro a Dir b, sen%s_b no se espera a registrar en este momento" % (num_sen+1))

            else:
                # print("Guardando registro a Dir b, sen%s_b" % (num_sen+1))
                # obteniendo la hora acutal
                hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                # Actulizando los datos utilizando el num. de rondas para colocarlo en su sitio correctamente, hora_now para hacer el registro y num_sen para su columna
                c.execute('''UPDATE b SET {} = ? where num_b = ? '''.format(sensor), (hora_now, ron_b[num_sen] ) )
                # Regresa esta respuesta a la funcion

    # Con esta linea se guardan los registros definitivamente el la bd
    conexion.commit()
    # cerrando conexiones con la bd
    conexion.close()

    # Imprime el estado de la rondas
    print('Las rondas terminan asi A', ron_a)
    print('Las rondas terminan asi B', ron_b)

    # Si todo salio bien
    return "ok"
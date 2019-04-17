# prom_past - Es una funcion para obtener un tiempo esperado la primera vez que se corre 'Modo evalaucion'
from datetime import datetime, timedelta
import datetime as dt
import sqlite3
import os.path

def prom_past( dir, num_sen, prom, bd ):
    dir = dir
    sen = num_sen
    prom = prom
    nombrebd = bd

    # Numero de rondas registradas en la BD
    ron_a = [ 0 , 0 , 0 ]
    ron_b = [ 0 , 0 , 0 ]

    # - Creando/Leyendo archivo de BD
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
    else:
        #!!!!! MENSAJE DE ERROR !!!!!!!!!!!!
        print("No exite este archivo", nombrebd)
        return 'Error!'

    # Leyendo datos de la bd
    if dir == 'a':
        # Asignado variables para obtener los datos
        n_sen = sen - 1
        ronda_ant = ron_a[n_sen] - 1
        nom_t = 'sen' + str(sen) + '_a'

        # Leer rondas y restar uno
        c.execute('SELECT {} FROM a WHERE num_a = ?'.format( nom_t ), ( ronda_ant, ))
        # Es decir ronda sen1 tiene 6 entradas, entonces seleccionar los datos de la 6 - 5
        bd_t = c.fetchone()

        tiempo = bd_t[0]

        # imprimiendo dato de tiempo
        print('Tiempo bd anterior',tiempo)

        #Tiempo promedio en segundos
        t_pro_s = int(prom)

        # Conversion a tiempo en h,m,s en datetime formato
        t_pro_f = dt.timedelta(seconds = t_pro_s)

        # Conversion de tiempo leido de la BD en datetime
        t_bd = datetime.strptime( tiempo , '%H:%M:%S')

        # TIEMPO ESPERADO
        t_esp = t_bd + t_pro_f

        print('Tiempo esperado/prom_pas',t_esp)
        return(t_esp)

    else:
        # Asignado variables para obtener los datos
        n_sen = sen - 1
        ronda_ant = ron_b[n_sen] - 1
        nom_t = 'sen' + str(sen) + '_b'

        # Leer rondas y restar uno
        c.execute('SELECT {} FROM b WHERE num_b = ?'.format( nom_t ), ( ronda_ant, ))        # Es decir ronda sen1 tiene 6 entradas, entonces seleccionar los datos de la 6 - 5
        bd_t = c.fetchone()

        # creando tiempo esperado
        tiempo = bd_t[0]

        #Tiempo promedio en segundos
        t_pro_s = int(prom)

        # Conversion a tiempo en h,m,s en datetime formato
        t_pro_f = dt.timedelta(seconds = t_pro_s)

        # Conversion de tiempo leido de la BD en datetime
        t_bd = datetime.strptime( tiempo , '%H:%M:%S')

        # TIEMPO ESPERADO
        t_esp = t_bd + t_pro_f

        print('Tiempo esperado/prom_pas',t_esp)
        return(t_esp)
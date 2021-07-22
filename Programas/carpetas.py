import csv
import os
from time import sleep
from pathlib import Path
import shutil


RUTA_CARPETA = "EVALUACIONES"
RUTA_ENTREGAS_ALUMNOS = f"{Path.home()}/Desktop/{RUTA_CARPETA}/"
CARGANDO = 0.15 #time.sleep()


def limpiar_pantalla() -> None:
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def ingresar_opcion(rango_opciones: int) -> int:
    '''
    PRE: El rango de opciones tiene que ser un número entero
    POST: Devuelve una opción representada por un número entero dentro del rango
    '''
    opcion = input(">>> Ingrese la opción:   ")
    while not (opcion.isnumeric() and 0 < int(opcion) <= rango_opciones):
        if rango_opciones == 1:
            opcion = input("Pulse 1 >>>   ")
        else:
            opcion = input(f"Ingrese una opcion entre 1 y {rango_opciones} >>>   ")

    return int(opcion)


def listar_archivos_carpeta_actual() -> None:
    
    '''
    PRE: --
    DESC: Permite listar todos los archivos que se encuentren en la carpeta actual y en las subcarpetas de la misma tanto a nivel local como remoto
    POST: --
    '''

    contenido = list()
    lista_carpetas = list()
    directorio = RUTA_ENTREGAS_ALUMNOS
    seguir = True

    while seguir:
        directorio_actual = os.path.normpath(directorio)

        for root, directorios, contenido in os.walk(directorio, topdown = False):
            for carpetas in directorios:
                lista_carpetas.append(carpetas)

            contenido = os.listdir(directorio)
                
        if len(lista_carpetas) == 0 and len(contenido) != 0:
            print("Archivos en esta carpeta: ")
            print(contenido)
            seguir = False
        elif len(contenido) == 0:
            print("Esta carpeta esta vacia!")
            seguir = False
        else:
            print(directorio_actual)
            print(f"{contenido}\n")
            print("1) Seguir entrando en las carpetas\n2) Volver atrás\n3) Detener el proceso")
            seguir_entrando = ingresar_opcion(3)

            if seguir_entrando == 1:

                carpeta = input("¿Cuál quiere acceder?")

                while carpeta not in directorios:
                    print("Esa carpeta no existe")
                    carpeta = input("Cual quiere acceder? ")
                    
                lista_carpetas.clear()
                directorio_carpeta = os.path.join(directorio, carpeta)
                directorio = directorio_carpeta
                
            elif seguir_entrando == 2:

                regresador = directorio_actual.split('\\')
                #['C:', 'Users', 'Nestor', 'Desktop', 'EVALUACIONES']
                regresador.pop(len(regresador) - 1)
                #['C:', 'Users', 'Nestor', 'Desktop']

                directorio_anterior = str()

                for i in range(len(regresador)):
                    directorio_anterior += regresador[i] + "\\"

                directorio = directorio_anterior
            else:
                seguir = False


def obtener_alumnos(ruta_alumnos: str) -> dict:

    '''
    PRE: La ruta tiene que existir
    DESC: Recibe csv alumnos y genera dict alumnos
    POST: --
    '''

    alumnos = dict()
    alumno_nombre = 1
    alumno_padron = 0
    alumno_mail = 2

    print("Obteniendo datos de los alumnos...")
    sleep(CARGANDO)

    with open(ruta_alumnos, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)
        
        for fila in csv_reader:
            alumnos[fila[alumno_padron]] = (fila[alumno_nombre], fila[alumno_mail])
    
    return alumnos


def obtener_docentes(ruta_docentes: str) -> None:

    '''
    PRE: La ruta tiene que existir
    DESC: Recibe csv docentes y genera dict docentes
    POST: --
    '''

    docentes = dict()
    docente_nombre = 0
    docente_mail = 1

    print("Obteniendo datos de los docentes...")
    sleep(CARGANDO)

    with open(ruta_docentes, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)

        for fila in csv_reader:
            docentes[fila[docente_nombre]] = fila[docente_mail]
    
    return docentes


def obtener_docente_y_alumnos(ruta_dya: str) -> dict:

    '''
    PRE: La ruta tiene que existir
    DESC: Recibe csv docentes-alumnos y genera dict docentes-alumnos (dya)
    POST: --
    '''   

    dya = dict()
    docentes_agregados = list()

    print("Obteniendo las relaciones docente <- alumnos...")
    sleep(CARGANDO)

    with open(ruta_dya, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)

        for fila in csv_reader:
            docente = fila[0]
            alumno = fila[1]

            if docente not in docentes_agregados:
                dya[docente] = [alumno]
                docentes_agregados.append(docente)
            else:
                dya[docente].append(alumno)
    
    return dya


def crear_carpetas_anidadas(nombre_evaluacion: str, alumnos: dict, entregas_alumnos: list, docentes: dict, dya: dict) -> None:

    '''
    PRE: Nombre de evaluación no nulo
    DESC: Recibe los diccionarios de los csv y crea las carpetas de docentes y alumnos
    POST: Carpetas anidadas creadas en el disco duro
    '''

    docentes_nombres = list(docentes.keys())
    alumnos_padrones = list(alumnos.keys())

    print("Creando las carpetas para los docentes...")
    sleep(CARGANDO)

    # Creamos las carpetas de los docentes
    for i in range(len(docentes_nombres)):
        try:
            os.makedirs(f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/{docentes_nombres[i]}')
        except FileExistsError:
            pass
    
    print("Anidando las carpetas de los alumnos...")
    sleep(CARGANDO)

    # Creamos las subcarpetas de alumnos
    # Si el docente no se encuentra en dya.csv, es porque no tiene un alumno asignado
    for docente in docentes_nombres:
        if docente in dya:
            for alumno in dya[docente]:
                try:
                    if alumno in entregas_alumnos:
                        try:
                            os.makedirs(f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/{docente}/{alumno} - {alumnos[alumno][0]}')
                        except FileExistsError:
                            pass
                except KeyError:
                    pass
    
    print("Ubicando alumnos sin docentes asignados...")
    sleep(CARGANDO)

    # Creamos las carpetas para los alumnos huérfanos (sin docentes)
    alumnos_asignados_aux = list(dya.values())
    alumnos_asignados = list()

    for i in range(len(alumnos_asignados_aux)):
        for j in range(len(alumnos_asignados_aux[i])):
            alumnos_asignados.append(alumnos_asignados_aux[i][j])

    for alumno in alumnos_padrones:
        if alumno not in alumnos_asignados:
            if alumno in entregas_alumnos:
                try:
                    os.makedirs(f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/(Sin docente asignado)/{alumno} - {alumnos[alumno][0]}')
                except FileExistsError:
                    pass
    
    # Borramos las carpetas de los docentes cuyos alumnos no hayan entregado nada
    carpetas = os.listdir(f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/')

    for carpeta in carpetas:
        carpeta_actual = f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/{carpeta}'
        try:
            if len(os.listdir(carpeta_actual)) == 0:
                try:
                    os.rmdir(carpeta_actual)
                except FileNotFoundError:
                    pass
                #print(f"Borrado directorio vacio {carpeta_actual}.")
        except FileNotFoundError:
            pass


def verificar_existencia_csv() -> None:

    '''
    PRE: --
    DESC: Comprueba que los archivos .csv con los datos de docentes y alumnos existan, y si no fuerza al usuario a encontrarlos
    POST: --
    '''

    alumnos_csv = False
    docentes_csv = False
    docentealumnos_csv = False

    # ¿Dejamos al usuario elegir la ubicación de la carpeta de la evaluación? Yo diría que no

    while not alumnos_csv or not docentes_csv or not docentealumnos_csv:
        ubicacion_csv = os.path.normpath(f'{RUTA_ENTREGAS_ALUMNOS}')
        input(f">>>>> Mueva los archivos alumnos.csv, docentes.csv y docente-alumnos.csv a {ubicacion_csv} y presione Enter:  ")
        print("\n")

        alumnos_csv = os.path.exists(f'{RUTA_ENTREGAS_ALUMNOS}/alumnos.csv')
        docentes_csv = os.path.exists(f'{RUTA_ENTREGAS_ALUMNOS}/docentes.csv')
        docentealumnos_csv = os.path.exists(f'{RUTA_ENTREGAS_ALUMNOS}/docente-alumnos.csv')


def crear_carpetas_evaluaciones(entregas_alumnos: list, nombre_evaluacion: str) -> None:

    '''
    PRE: Nombre de la evaluación no nulo
    DESC: Recibe los csv de los docentes, los alumnos que entregaron y los alumnos asignados a cada docente, además de las entregas de los alumnos
    POST: Carpetas anidadas creadas
    '''
    
    entregas_alumnos_2 = list()

    if entregas_alumnos != None:
        for i in range(len(entregas_alumnos)):
            entregas_alumnos_2.append(entregas_alumnos[i].split("  ")[0])

    verificar_existencia_csv()
    limpiar_pantalla()

    datos = {"alumnos.csv":f"{RUTA_ENTREGAS_ALUMNOS}/alumnos.csv", 
             "docentes.csv":f"{RUTA_ENTREGAS_ALUMNOS}/docentes.csv", 
             "docente-alumnos.csv":f"{RUTA_ENTREGAS_ALUMNOS}/docente-alumnos.csv"}
           # "nombre_archivo.csv":"ruta_del_archivo.csv",
    
    alumnos = obtener_alumnos(datos["alumnos.csv"])
    docentes = obtener_docentes(datos["docentes.csv"])
    dya = obtener_docente_y_alumnos(datos["docente-alumnos.csv"])
    crear_carpetas_anidadas(nombre_evaluacion, alumnos, entregas_alumnos_2, docentes, dya)


def copiar_csv_prueba() -> None:

    # Usamos los .csv de prueba (copia automática al directorio correspondiente)
    
    ubicacion_csv = os.getcwd()
    carpeta_actual = os.getcwd().split("\\")[ len(os.getcwd().split("\\")) - 1 ]

    if carpeta_actual == "TP2_APIS":
        ubicacion_csv = f'{os.getcwd()}/Programas/'
    elif carpeta_actual == "Programas":
        ubicacion_csv = f'{os.getcwd()}/'
    else:
        ubicacion_csv == f'{Path.home()}/TP2_APIS/Programas'

    datos = [f'{ubicacion_csv}/alumnos.csv', f'{ubicacion_csv}/docentes.csv', f'{ubicacion_csv}/docente-alumnos.csv']
    
    try:
        os.makedirs(RUTA_ENTREGAS_ALUMNOS)
    except Exception:
        pass
    
    for i in range(len(datos)):
        shutil.copy(datos[i], RUTA_ENTREGAS_ALUMNOS)
    
    #print(f"Se copiaron los .csv de prueba exitosamente a {RUTA_ENTREGAS_ALUMNOS}.")


def main() -> None:
    copiar_csv_prueba()


main()


# -----------------------------------------------------------------------------------------------------


# ESTA FUNCIÓN SE LLAMARÁ DESDE main.py

# ENTREGAS_ALUMNOS = ['108244  Palavecino, Nestor', '847384  Valle, Adrian', '101010  Richardson, Juan']
# crear_carpetas_evaluaciones(ENTREGAS_ALUMNOS, "Recuperatorio")


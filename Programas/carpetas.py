import csv
import os
import archivos


def imprimir_diccionario_simple(diccionario: dict) -> None:
    for elemento in diccionario:
        print(f"{elemento}: {diccionario[elemento]}")

    print("\n\n")


def obtener_evaluaciones(ruta_evaluaciones: str) -> dict:
    # Recibe csv evaluaciones y genera dict evaluaciones
    evaluaciones = dict()
    evaluacion_nombre = 0
    finalizado = 1

    with open(ruta_evaluaciones, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)
        for fila in csv_reader:
            evaluaciones[fila[evaluacion_nombre]] = fila[finalizado]

    return evaluaciones


def obtener_alumnos(ruta_alumnos: str) -> dict:
    # Recibe csv alumnos y genera dict alumnos
    alumnos = dict()
    alumno_nombre = 0
    alumno_padron = 1
    alumno_mail = 2

    with open(ruta_alumnos, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)
        for fila in csv_reader:
            alumnos[fila[alumno_nombre]] = (fila[alumno_padron], fila[alumno_mail])
    
    return alumnos


def obtener_docentes(ruta_docentes: str) -> None:
    # Recibe csv docentes y genera dict docentes
    docentes = dict()
    docente_nombre = 0
    docente_mail = 1

    with open(ruta_docentes, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)
        for fila in csv_reader:
            docentes[fila[docente_nombre]] = fila[docente_mail]
    
    return docentes


def obtener_docente_y_alumnos(ruta_dya: str) -> dict:
    # Recibe csv docentes-alumnos y genera dict docentes-alumnos (dya)
    dya = dict()
    docentes_agregados = list()

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


def crear_carpetas_anidadas(evaluaciones: dict, alumnos: dict, docentes: dict, dya: dict) -> None:
    # Recibe los csv y crea las carpetas

    docentes_nombres = list(docentes.keys())
    alumnos_nombres = list(alumnos.keys())

    # Creamos las carpetas para cada evaluación
    for evaluacion in evaluaciones:

        # Creamos las carpetas de los docentes
        for i in range(len(docentes_nombres)):
            try:
                os.makedirs(f'Evaluaciones/{evaluacion}/{docentes_nombres[i]}')
            except FileExistsError:
                pass
        
        # Creamos las subcarpetas de alumnos
        # Si el docente no se encuentra en dya.csv, es porque no tiene un alumno asignado
        for docente in docentes_nombres:
            if docente in dya:
                for alumno in dya[docente]:
                    try:
                        os.makedirs(f'Evaluaciones/{evaluacion}/{docente}/{alumno}')
                    except FileExistsError:
                        pass
        
        # Creamos las carpetas para los alumnos huérfanos (sin docentes)
        alumnos_asignados_aux = list(dya.values())
        alumnos_asignados = list()
        for i in range(len(alumnos_asignados_aux)):
            for j in range(len(alumnos_asignados_aux[i])):
                alumnos_asignados.append(alumnos_asignados_aux[i][j])

        for alumno in alumnos_nombres:
            if alumno not in alumnos_asignados:
                try:
                    os.makedirs(f'Evaluaciones/{evaluacion}/(Sin docente asignado)/{alumno}')
                except FileExistsError:
                    pass


def colocar_evaluaciones(evaluaciones: str, entregas_alumnos: str):
    # Acá se copia cada archivo .zip desde "/entregas_alumnos" a su carpeta de alumno correspondiente,
    # Además verifica que la evaluación se encuentre en la lista de evaluaciones

    # Posible función para asignar a Tomi.
    '''
    ZIP_PRUEBA = os.getcwd() + f"/{entregas_alumnos}/321323 - Juarez, Pepe.zip"
    archivos.descompresor(ZIP_PRUEBA) # necesito poder pasar parámetro de ruta de descompresión
    '''
    pass


def organizar_evaluaciones(datos: dict, entregas_alumnos: str) -> None:

    # Recibe los csv de las evaluaciones, los docentes, los alumnos y los alumnos asignados a cada docente,
    # además de las entregas de los alumnos
    
    evaluaciones = obtener_evaluaciones(datos["evaluaciones.csv"])
    alumnos = obtener_alumnos(datos["alumnos.csv"])
    docentes = obtener_docentes(datos["docentes.csv"])
    dya = obtener_docente_y_alumnos(datos["docente-alumnos.csv"])

    '''
    imprimir_diccionario_simple(alumnos)
    imprimir_diccionario_simple(docentes)
    imprimir_diccionario_simple(dya)
    '''

    crear_carpetas_anidadas(evaluaciones, alumnos, docentes, dya)
    colocar_evaluaciones(evaluaciones, entregas_alumnos)


# --------------------------------------------------------------------------

# USO ARCHIVOS CSV DE PRUEBA (ADJUNTO LOS ARCHIVOS AL GITHUB)

DATOS = datos = {"evaluaciones.csv":"evaluaciones.csv", 
                 "alumnos.csv":"alumnos.csv", 
                 "docentes.csv":"docentes.csv", 
                 "docente-alumnos.csv":"docente-alumnos.csv"}
               # "nombre_archivo.csv":"ruta_del_archivo.csv",

RUTA_ENTREGAS_ALUMNOS = "/entregas_alumnos"  # LLENO DE .ZIPS

# ESTA FUNCIÓN SE LLAMARÁ DESDE main.py
organizar_evaluaciones(DATOS, RUTA_ENTREGAS_ALUMNOS)
import csv
import os
import archivos


# USO ARCHIVOS CSV DE PRUEBA (ADJUNTO LOS ARCHIVOS AL GITHUB)

RUTA_ENTREGAS_ALUMNOS = "/entregas_alumnos"  # LLENO DE .ZIPS
RUTA_EVALUACIONES = "evaluaciones.csv"
RUTA_ALUMNOS = "alumnos.csv"
RUTA_DOCENTES = "docentes.csv"
RUTA_DYA = "docente-alumnos.csv"


def imprimir_diccionario_simple(diccionario: dict, forma: int = 1) -> None:
    if forma == 1:
        for elemento in diccionario:
            print(f"{elemento}: {diccionario[elemento]}")
    elif forma == 2:
        for clave, valor in diccionario.items():
            print(f"{clave}: {valor}")
    
    print("\n\n")


def obtener_evaluaciones(evaluaciones_csv: str) -> dict:
    pass


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

    # Creamos las carpetas de los docentes
    for i in range(len(docentes_nombres)):
        try:
            os.mkdir(docentes_nombres[i])
        except FileExistsError:
            pass
    
    # Creamos las subcarpetas de alumnos
    # Si el docente no se encuentra en dya.csv, es porque no tiene un alumno asignado
    for docente in docentes_nombres:
        if docente in dya:
            for alumno in dya[docente]:
                try:
                    os.makedirs(f'{docente}/{alumno}')
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
                os.makedirs(f'(Sin docente asignado)/{alumno}')
            except FileExistsError:
                pass


def colocar_evaluaciones(evaluaciones: str, entregas_alumnos: str):
    # Acá se copia cada archivo .zip desde "/entregas_alumnos" a su carpeta de alumno correspondiente,
    # Además verifica que la evaluación se encuentre en la lista de evaluaciones

    # Posible función para asignar a Tomi.
    pass


def organizar_evaluaciones(entregas_alumnos: str, evaluaciones_csv: str, alumnos_csv: str, docentes_csv: str, dya_csv: str) -> None:

    # Recibe los csv de las evaluaciones, los docentes, los alumnos y los alumnos asignados a cada docente,
    # además de las entregas de los alumnos

    alumnos = obtener_alumnos(alumnos_csv)
    docentes = obtener_docentes(docentes_csv)
    dya = obtener_docente_y_alumnos(dya_csv)
    evaluaciones = obtener_evaluaciones(evaluaciones_csv)

    '''
    imprimir_diccionario_simple(alumnos)
    imprimir_diccionario_simple(docentes)
    imprimir_diccionario_simple(dya)
    '''

    crear_carpetas_anidadas(evaluaciones, alumnos, docentes, dya)
    colocar_evaluaciones(evaluaciones, entregas_alumnos)


# ESTA FUNCIÓN SE LLAMARÁ DESDE main.py
organizar_evaluaciones(RUTA_ENTREGAS_ALUMNOS, RUTA_EVALUACIONES, RUTA_ALUMNOS, RUTA_DOCENTES, RUTA_DYA)


'''
Crear directorios:

    os.mkdir('dir1')
    os.makedirs('dir1/dir2/dir3')
'''

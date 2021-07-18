import csv
import os
from pathlib import Path


RUTA_CARPETA = "EVALUACIONES"
RUTA_ENTREGAS_ALUMNOS = f"{Path.home()}/Desktop/{RUTA_CARPETA}/"


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


def crear_carpetas_anidadas(nombre_evaluacion: str, alumnos: dict, entregas_alumnos: list, docentes: dict, dya: dict) -> None:
    # Recibe los csv y crea las carpetas

    docentes_nombres = list(docentes.keys())
    alumnos_nombres = list(alumnos.keys())

    # Creamos las carpetas de los docentes
    for i in range(len(docentes_nombres)):
        try:
            os.makedirs(f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/{docentes_nombres[i]}')
        except FileExistsError:
            pass
    
    # Creamos las subcarpetas de alumnos
    # Si el docente no se encuentra en dya.csv, es porque no tiene un alumno asignado
    for docente in docentes_nombres:
        if docente in dya:
            for alumno in dya[docente]:
                if alumno in entregas_alumnos:
                    try:
                        os.makedirs(f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/{docente}/{alumno}')
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
            if alumno in entregas_alumnos:
                try:
                    os.makedirs(f'{RUTA_ENTREGAS_ALUMNOS}/{nombre_evaluacion}/(Sin docente asignado)/{alumno}')
                except FileExistsError:
                    pass


def crear_carpetas_evaluaciones(entregas_alumnos: list, nombre_evaluacion: str) -> None:
    # Recibe los csv de los docentes, los alumnos que entregaron y los alumnos asignados a cada docente,
    # además de las entregas de los alumnos

    entregas_alumnos_2 = dict()
    entregas_alumnos_3 = list()

    if entregas_alumnos != None:
        for i in range(len(entregas_alumnos)):
            entregas_alumnos_2[entregas_alumnos[i][0:6:1]] = entregas_alumnos[i][8 : len(entregas_alumnos[i]) : 1]

    for elemento in entregas_alumnos_2:
        entregas_alumnos_3.append(entregas_alumnos_2[elemento])

    datos = {"alumnos.csv":f"{RUTA_ENTREGAS_ALUMNOS}/alumnos.csv", 
             "docentes.csv":f"{RUTA_ENTREGAS_ALUMNOS}/docentes.csv", 
             "docente-alumnos.csv":f"{RUTA_ENTREGAS_ALUMNOS}/docente-alumnos.csv"}
               # "nombre_archivo.csv":"ruta_del_archivo.csv",
    
    alumnos = obtener_alumnos(datos["alumnos.csv"])
    docentes = obtener_docentes(datos["docentes.csv"])
    dya = obtener_docente_y_alumnos(datos["docente-alumnos.csv"])
    crear_carpetas_anidadas(nombre_evaluacion, alumnos, entregas_alumnos_3, docentes, dya)


# -----------------------------------------------------------------------------------------------------





# ESTA FUNCIÓN SE LLAMARÁ DESDE main.py
''''
ENTREGAS_ALUMNOS = ['107411  Hernandez, Jose', '789456  Villegas, Tomas']
crear_carpetas_evaluaciones(ENTREGAS_ALUMNOS, "Recuperatorio")
'''

'''
from pathlib import Path
home = str(Path.home())

print(home)
'''

'''
import time
time.sleep(16)
'''
import csv
import os


# USO ARCHIVOS CSV DE PRUEBA (ADJUNTO LOS ARCHIVOS AL GITHUB)


RUTA_ALUMNOS = "alumnos.csv"
ALUMNO_NOMBRE = 0
ALUMNO_PADRON = 1
ALUMNO_MAIL = 2

RUTA_DOCENTES = "docentes.csv"
DOCENTE_NOMBRE = 0
DOCENTE_MAIL = 1

RUTA_DYA = "docente-alumnos.csv"
DYA_DOCENTE_NOMBRE = 0
DYA_ALUMNO_NOMBRE = 1


def obtener_alumnos() -> dict:
    # Recibe csv alumnos y genera dict alumnos
    alumnos = dict()

    with open(RUTA_ALUMNOS, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)
        for fila in csv_reader:
            alumnos[fila[ALUMNO_NOMBRE]] = (fila[ALUMNO_PADRON], fila[ALUMNO_MAIL])
    
    return alumnos


def obtener_docentes() -> None:
    # Recibe csv docentes y genera dict docentes
    docentes = dict()

    with open(RUTA_DOCENTES, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)
        for fila in csv_reader:
            docentes[fila[DOCENTE_NOMBRE]] = fila[DOCENTE_MAIL]
    
    return docentes


def obtener_docente_y_alumnos() -> dict:
    # Recibe csv docentes-alumnos y genera dict docentes-alumnos (dya)
    docentes = dict()

    with open(RUTA_DYA, mode='r', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter= ';')
        next(csv_reader)
        for fila in csv_reader:
            docentes[fila[DYA_DOCENTE_NOMBRE]] = fila[DYA_ALUMNO_NOMBRE]
    
    return docentes


def crear_carpetas_anidadas(alumnos: dict, docentes: dict, dya: dict) -> None:
    # Recibe los csv y crea las carpetas
    "Nota: crear carpetas para docentes sin alumnos y ubicar a los alumnos sin docentes en una carpeta aparte"
    docentes_nombres = list(docentes.keys())
    alumnos_nombres = list(alumnos.keys())

    # Creamos las carpetas aquí
    for i in range(len(docentes_nombres)):
        #os.mkdir(docentes_nombres[i])
        #os.mkdir("(Sin docente asignado)")
        pass


def generar_carpetas_evaluacion(nombre_evaluacion: str="", entrega_alumnos: dict=(), docentes_csv: str="", dya_csv: str="") -> None:
    # Recibe el nombre de la evaluación (ej: "2021-06-15"), 
    # la entrega de los alumnos (archivo .zip) y los .csv de los docentes-alumnos
    alumnos = obtener_alumnos()
    docentes = obtener_docentes()
    dya = obtener_docente_y_alumnos()
    print(alumnos, docentes, dya) #debug
    crear_carpetas_anidadas(alumnos, docentes, dya)


generar_carpetas_evaluacion()


'''
Crear directorios:

    os.mkdir('dir1')
    os.makedirs('dir1/dir2/dir3')
'''

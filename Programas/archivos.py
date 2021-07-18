#Me encargo de los archivos - Tomas
import os
import zipfile
import tempfile
import csv
import shutil
from pathlib import Path

RUTA_CARPETA = "EVALUACIONES"
FORMATOS_DE_ARCHIVOS = [".py",".txt",".csv"]
DIRECTORIO_DE_INICIO = f"{Path.home()}/Desktop/{RUTA_CARPETA}/"

def verificador_de_archivo_mas_nuevo(archivo_local:str,archivo_drive:str)->None:
        archivo_mas_nuevo = ""

        if os.path.st_mtime_ns(archivo_local) < os.path.st_mtime_ns(archivo_drive):
            archivo_mas_nuevo = archivo_local

        elif os.path.st_mtime_ns(archivo_drive) < os.path.st_mtime_ns(archivo_local):
            archivo_mas_nuevo = archivo_drive

        return archivo_mas_nuevo


def mover_archivo(direccion_del_archivo_original:str,nombre_del_archivo:str,directorio_de_inicio)->None:
    #NO FUE TESTEADA TODAVIA
    nuevo_directorio = ("Dar el nuevo directorio: ")

    if nuevo_directorio in directorio_de_inicio:
        nueva_direccion_del_archivo = os.path.join(nuevo_directorio, nombre_del_archivo)
        shutil.move(direccion_del_archivo_original,nueva_direccion_del_archivo)


def copiador_de_archivos(archivo_a_copiar:str,archivo_a_reemplazar:str)->None:
    #NO FUE TESTEADA tODAVIA
    with open(archivo_a_copiar,"r"):
        with open(archivo_a_reemplazar,"w"):
            archivo_a_reemplazar.write(archivo_a_copiar)


def descompresor(zip:str)->None:
        nombre_del_corrector = str()

        archivo = os.path.basename(zip)
        archivo_separado = os.path.splitext(archivo)
        nombre_del_alumno = archivo_separado[0].split(" - ")
        
        with open ("Programas/docente-alumnos.csv", mode="r") as archivo_csv:
            csv_reader = csv.reader(archivo_csv, delimiter= ";")
            next(csv_reader)
            for linea in csv_reader:
                if nombre_del_alumno[1] == linea[1]:
                    nombre_del_corrector = linea[0]

        for root, directorios, archivos in os.walk(DIRECTORIO_DE_INICIO, topdown=False):
            for carpeta in directorios:
                if nombre_del_corrector == carpeta:
                    direccion_de_la_carpeta = os.path.join(root, nombre_del_corrector)
                    direccion_final = os.path.join(direccion_de_la_carpeta, nombre_del_alumno[1])
                    with zipfile.ZipFile(zip, 'r') as zip:
                        zip.extractall(direccion_final)
        
      
        
        

def buscador_de_archivos(directorio_de_inicio:str, nombre_del_archivo:str)->str:
    direccion_del_archivo = ""
    
    for root, directorios, archivos in os.walk(directorio_de_inicio, topdown=False):
        for archivo in archivos:
            if archivo == nombre_del_archivo:
                direccion_del_archivo = os.path.join(root, archivo)
    
    return direccion_del_archivo


def buscar_y_descomprimir(directorio_de_inicio:str, lista_de_archivos:list)->None:
    for archivo in lista_de_archivos:
        direccion_del_archivo = buscador_de_archivos(directorio_de_inicio, archivo)
        descompresor(direccion_del_archivo)


def sincronizacion(direccion:str, directorio_de_inicio:str)->None:
    direccion_del_archivo_mas_nuevo = ""
    no_seguir_descargando = False
    
    with tempfile.TemporaryDirectory(prefix="Drive-") as tmpdir:
        
        while not no_seguir_descargando:
            #funcion de descargar de drive
            ans = input("Queres seguir descargando? s/n ")
            if ans == "n":
                no_seguir_descargando = True
        
        with open("archivos_descargados.csv", "w") as archivo_csv:
            escribir = csv.writer(archivo_csv)
            escribir.writerow("Nombre de Archivo")
            for root, dirs, files in os.walk(tmpdir):
                for filename in files:
                    escribir.writerow(['', os.path.join(root,filename)])            
        
        with open("archivos_descargados.csv", "r") as archivo_csv:
            archivo_csv.next()
            for nombre_del_archivo in archivo_csv:
                direccion_del_archivo_local = buscador_de_archivos(directorio_de_inicio,nombre_del_archivo)
                direccion_del_archivo_drive = buscador_de_archivos(tmpdir, nombre_del_archivo)
                direccion_del_archivo_mas_nuevo = verificador_de_archivo_mas_nuevo(direccion_del_archivo_local,direccion_del_archivo_drive)
        
        #funcion para sUbir el archivo mas nuevo a drive
        copiador_de_archivos(direccion_del_archivo_mas_nuevo,direccion_del_archivo_local)


def crear_archivos(directorio_de_guardado:str, directorio_de_inicio:str)->None:
    dejar_de_crear_archivos = False
    while not dejar_de_crear_archivos:
        nombre_del_archivo = input("Decime el nombre del archivo: ")
        print (f"Estos son los tipos de extension validos: {FORMATOS_DE_ARCHIVOS}")
        extension = input("Decime una extension valida: ")

        if extension in FORMATOS_DE_ARCHIVOS:
            archivo = nombre_del_archivo + extension
            archivo_existente = buscador_de_archivos(directorio_de_inicio,archivo)
            
            if not archivo_existente  == "":
                print("Error: Archivo ya existe")
            
            else:
                direccion_del_archivo = os.path.join(directorio_de_guardado, archivo)
                open(direccion_del_archivo, "x")
                print("Archivo creado")        
                mover_archivo = input("Queres mover el archivo? s/n ")
                if mover_archivo == "s":
                    mover_archivo(direccion_del_archivo,archivo)
            seguir_creando =  int(input("1. Crear otro archivo 2. Dejar de Crear"))
            if seguir_creando == 2:
                dejar_de_crear_archivos = True

        else:
            print("Error: Extension No Valida")


def main()->None:
    directorio = "C:/Users/tomis/Desktop/UBA/Testeo/TP2/Juan_Perez/Puntin2/107411 - Hernandez, Jose.zip"
    descompresor(directorio)
main()

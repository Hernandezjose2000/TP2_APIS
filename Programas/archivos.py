#Me encargo de los archivos - Tomas
import os
import zipfile
import tempfile
import csv
import shutil
from pathlib import Path


FORMATOS_DE_ARCHIVOS = [".py",".txt",".csv"]


def verificador_de_archivo_mas_nuevo(archivo_local: str, archivo_drive: str) -> None:
        archivo_mas_nuevo = ""

        #if os.path.getmtime(archivo_local) < os.path.getmtime(archivo_drive):, tal vez?

        if os.path.st_mtime_ns(archivo_local) < os.path.st_mtime_ns(archivo_drive):
            archivo_mas_nuevo = archivo_local

        elif os.path.st_mtime_ns(archivo_drive) < os.path.st_mtime_ns(archivo_local):
            archivo_mas_nuevo = archivo_drive

        return archivo_mas_nuevo


def mover_archivo(direccion_del_archivo_original: str, nombre_del_archivo: str, directorio_de_inicio: str) -> None:
    nuevo_directorio = ("Dar el nuevo directorio: ")

    if nuevo_directorio in directorio_de_inicio:
        nueva_direccion_del_archivo = os.path.join(nuevo_directorio, nombre_del_archivo)
        shutil.move(direccion_del_archivo_original,nueva_direccion_del_archivo)


def copiador_de_archivos(archivo_a_copiar: str, archivo_a_reemplazar: str) -> None:
    try:
        with open(archivo_a_copiar,"r"):
            with open(archivo_a_reemplazar,"w"):
                archivo_a_reemplazar.write(archivo_a_copiar)
                
    except:
        print("No existe el archivo que quiere copiar o reemplazar o no esta en el directorio de Evaluaciones")


def descompresor(zip: str,directorio_de_inicio) -> None:
        archivo = os.path.basename(zip)
        #print(archivo)
        archivo_separado = os.path.splitext(archivo)
        #print(archivo_separado)
        nombre_del_alumno = archivo_separado[0].split("  ")
        print("- " + nombre_del_alumno[1])

        for root, directorios, archivos in os.walk(directorio_de_inicio, topdown=False):
            for carpeta in directorios:
                if nombre_del_alumno[0] == carpeta.split(" - ")[0]:
                    direccion_final = os.path.join(root, carpeta)

                    try:
                        with zipfile.ZipFile(zip, 'r') as zip:
                            zip.extractall(direccion_final)
                    except Exception:
                        pass
        

def buscador_de_archivos(directorio_de_inicio: str, nombre_del_archivo: str) -> str:
    direccion_del_archivo = ""
    
    for root, directorios, archivos in os.walk(directorio_de_inicio, topdown=False):
        for archivo in archivos:
            if archivo == nombre_del_archivo:
                direccion_del_archivo = os.path.join(root, archivo)
    
    return direccion_del_archivo


def buscar_y_descomprimir(directorio_de_inicio: str, lista_de_archivos: list) -> None:
    print("\n>>>>> Se encontraron nuevas entregas de los siguientes alumnos:\n")

    for archivo in lista_de_archivos:
        archivo = archivo + ".zip"
        direccion_del_archivo = buscador_de_archivos(directorio_de_inicio, archivo)
        descompresor(direccion_del_archivo, directorio_de_inicio)


def sincronizacion(direccion: str, directorio_de_inicio: str) -> None:
    direccion_del_archivo_local = ""
    direccion_del_archivo_drive = ""
    direccion_del_archivo_mas_nuevo = ""
    
    for archivo in direccion:
        with open("archivos_descargados.csv", "w") as archivo_csv:
            escribir = csv.writer(archivo_csv)
            escribir.writerow("Nombre de Archivo")
            for root, dirs, files in os.walk(direccion):
                for filename in files:
                    escribir.writerow(['', os.path.join(root,filename)])            
            
    with open("archivos_descargados.csv", "r") as archivo_csv:
        next(archivo_csv)
        for nombre_del_archivo in archivo_csv:
            direccion_del_archivo_local = buscador_de_archivos(directorio_de_inicio, nombre_del_archivo)
            direccion_del_archivo_drive = buscador_de_archivos(direccion, nombre_del_archivo)
            direccion_del_archivo_mas_nuevo = verificador_de_archivo_mas_nuevo(direccion_del_archivo_local, direccion_del_archivo_drive)
            
    copiador_de_archivos(direccion_del_archivo_mas_nuevo,direccion_del_archivo_local)
    
    return direccion_del_archivo_mas_nuevo 


def crear_archivos(directorio_de_inicio: str) -> None:
    dejar_de_crear_archivos = False

    try:
        os.makedirs(f"{directorio_de_inicio}/archivos_creados")
    except FileExistsError:
        pass

    nombre_del_archivo = input("Decime el nombre del archivo: ")
    print (f"Estos son los tipos de extension validos: {FORMATOS_DE_ARCHIVOS}")
    extension = input("Decime una extension valida: ")

    while extension not in FORMATOS_DE_ARCHIVOS:
        print("Error: Extension No Valida")
        extension = input("Decime una extension valida: ")

    archivo = nombre_del_archivo + extension
    archivo_existente = buscador_de_archivos(directorio_de_inicio,archivo)
            
    if not archivo_existente  == "":
        print('''Error: Archivo ya existe \nLa direccion del archivo es {archivo_existente}. 
        (Copie esta direccion para poder subir el archivo al Drive)''')
        
            
    else:
        direccion_del_archivo = os.path.join(f"{directorio_de_inicio}/archivos_creados", archivo)
        os.path.normpath(directorio_de_inicio)
        open(direccion_del_archivo, "x")
        print(f"Archivo creado, direccion: {direccion_del_archivo} \n(Copie esta direccion para poder subir el archivo al Drive)")        
            
# (Pala): me arrojaba esto: AttributeError: module 'ntpath' has no attribute 'st_mtime_ns'
        
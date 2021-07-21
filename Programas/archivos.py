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


def mover_archivo(direccion_del_archivo_original:str,nombre_del_archivo:str,directorio_de_inicio:str)->None:
    nuevo_directorio = ("Dar el nuevo directorio: ")

    if nuevo_directorio in directorio_de_inicio:
        nueva_direccion_del_archivo = os.path.join(nuevo_directorio, nombre_del_archivo)
        shutil.move(direccion_del_archivo_original,nueva_direccion_del_archivo)


def copiador_de_archivos(archivo_a_copiar:str,archivo_a_reemplazar:str)->None:
    try:
        with open(archivo_a_copiar,"r"):
            with open(archivo_a_reemplazar,"w"):
                archivo_a_reemplazar.write(archivo_a_copiar)
                
    except:
        print("No existe el archivo que quiere copiar o reemplazar o no esta en el directorio de Evaluaciones")


def descompresor(zip:str) -> None:
        archivo = os.path.basename(zip)
        #print(archivo)
        archivo_separado = os.path.splitext(archivo)
        #print(archivo_separado)
        nombre_del_alumno = archivo_separado[0].split("  ")
        print(nombre_del_alumno[1])

        for root, directorios, archivos in os.walk(DIRECTORIO_DE_INICIO, topdown=False):
            for carpeta in directorios:
                if nombre_del_alumno[0] == carpeta.split(" - ")[0]:
                    direccion_final = os.path.join(root, carpeta)

                    #try agregado como prueba
                    try:
                        with zipfile.ZipFile(zip, 'r') as zip:
                            zip.extractall(direccion_final)
                    except Exception:
                        pass
        

def buscador_de_archivos(directorio_de_inicio:str, nombre_del_archivo:str)->str:
    direccion_del_archivo = ""
    
    for root, directorios, archivos in os.walk(directorio_de_inicio, topdown=False):
        for archivo in archivos:
            if archivo == nombre_del_archivo:
                direccion_del_archivo = os.path.join(root, archivo)
    
    return direccion_del_archivo


def buscar_y_descomprimir(directorio_de_inicio:str, lista_de_archivos:list) -> None:
    print("\nSe encontraron nuevas entregas de los alumnos:\n")

    for archivo in lista_de_archivos:
        archivo = archivo +".zip"
        direccion_del_archivo = buscador_de_archivos(directorio_de_inicio, archivo)
        descompresor(direccion_del_archivo)


def sincronizacion(direccion:str, directorio_de_inicio:str)->None:
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
            direccion_del_archivo_local = buscador_de_archivos(directorio_de_inicio,nombre_del_archivo)
            direccion_del_archivo_drive = buscador_de_archivos(direccion, nombre_del_archivo)
            direccion_del_archivo_mas_nuevo = verificador_de_archivo_mas_nuevo(direccion_del_archivo_local,direccion_del_archivo_drive)
            
    copiador_de_archivos(direccion_del_archivo_mas_nuevo,direccion_del_archivo_local)
    
    return direccion_del_archivo_mas_nuevo 



def crear_archivos(directorio_de_guardado:str, directorio_de_inicio:str)->None:
    dejar_de_crear_archivos = False
    while not dejar_de_crear_archivos:
        nombre_del_archivo = input("Decime el nombre del archivo: ")
        print (f"Estos son los tipos de extension validos: {FORMATOS_DE_ARCHIVOS}")
        extension = input("Decime una extension valida: ")

        while extension not in FORMATOS_DE_ARCHIVOS:
            print("Error: Extension No Valida")
            extension = input("Decime una extension valida: ")

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

        
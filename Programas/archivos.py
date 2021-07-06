#Me encargo de los archivos - Tomas
import os
import tempfile
import zipfile

def verificador_de_archivos(archivo_local:str,archivo_drive:str)->list:
    #for archivo1 in carpeta1:
        if os.path.st_mtime_ns(archivo_local) < os.path.st_mtime_ns(archivo_drive):
            copiador_de_archivos(archivo_local,archivo_drive)
        elif os.path.st_mtime_ns(archivo_drive) < os.path.st_mtime_ns(archivo_local):
            copiador_de_archivos(archivo_drive,archivo_local)

def copiador_de_archivos(archivo_a_copiar:str,archivo_a_reemplazar:str)->None:
    with open(archivo_a_copiar,"r"):
        with open(archivo_a_reemplazar,"w"):
            archivo_a_reemplazar.write(archivo_a_copiar)

def descompresor(zip:str)->None:
    with zipfile.ZipFile(zip, 'r') as zip:
        zip.extractall()

def buscador_de_archivos(directorio_de_inicio:str, nombre_del_archivo:str)->None:
    for root, files in os.walk(directorio_de_inicio, topdown=False):
        for name in files:
            if name == nombre_del_archivo:
                print(os.path.join(root, name))



#with tempfile.TemporaryDirectory(prefix="Drive-") as tmpdir:

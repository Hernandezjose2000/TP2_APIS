# TRABAJO PRÁCTICO N°2 DE ALGORITMOS Y PROGRAMACIÓN I

import archivos
import carpetas
#import drive     
#import gmail
import os
import time

'''
    Python ejecuta los archivos al importarlos, así que hay que colocar los client_secret en la misma carpeta que main.py,
    o el programa no va a funcar porque no los encuentra
'''


def ingresar_opcion_int(rango_opciones: int) -> int:
    opcion = input(">>> Ingrese la opción:   ")
    while not (opcion.isnumeric() and 0 < int(opcion) <= rango_opciones):
        if rango_opciones == 1:
            opcion = input("Pulse 1 >>>   ")
        else:
            opcion = input(f"Ingrese una opcion entre 1 y {rango_opciones} >>>   ")
    return int(opcion)


def listar_archivos_carpeta_actual() -> None:
    print("Seleccione donde desea ver sus archivos: ")
    print("1 - Google Drive")
    print("2 - Mi PC")
    print("3 - Atrás")

    opcion = ingresar_opcion_int(3)
    
    if opcion == 1:
        # drive.explorar_archivos()
        pass
    elif opcion == 2:
        # archivos.explorar_archivos()
        pass


def crear_archivo() -> None:
    print("Seleccione donde desea crear un archivo o carpeta: ")
    print("1 - Google Drive")
    print("2 - Mi PC")
    print("3 - Atrás")

    opcion = ingresar_opcion_int(3)
    
    if opcion == 1:
        # drive.crear_archivo()
        pass
    elif opcion == 2:
        # archivos.crear_archivo()
        pass


def subir_archivo() -> None:
    # drive.subir_archivo()
    pass

def descargar_archivo() -> None:
    # drive.descargar_archivo()
    pass

def sincronizar() -> None:
    # carpetas.sincronizar()
    pass


def generar_carpetas_evaluacion() -> None:
    datos = {"evaluaciones.csv":"ruta", "alumnos.csv":"ruta", "docentes.csv":"ruta", "docente-alumnos.csv":"ruta"}

    for nombre in datos:
        print(f"Buscando el archivo '{nombre}'...")
        time.sleep(1.5)
        datos[nombre] = archivos.buscador_de_archivos(os.getcwd(), nombre)
    
    print("Se han encontrado todos los archivos.")

    #entregas_alumnos = archivos.buscador_de_carpetas(os.getcwd(), "entregas_alumnos")
    entregas_alumnos = "/entregas_alumnos"

    carpetas.organizar_evaluaciones(datos, entregas_alumnos)

    print("Se han creado o agregado las carpetas de las evaluaciones exitosamente.")


def actualizar_entregas_alumnos() -> None:
    pass


def menu() -> None:
    continuar_en_menu = True

    while continuar_en_menu:
        print("GOOGLE DRIVE - LOCAL\n")
        print("1 - Listar archivos de la carpeta actual")
        print("2 - Crear un archivo")
        print("3 - Subir un archivo")
        print("4 - Descargar un archivo")
        print("5 - Sincronizar\n\n")

        print("SISTEMA DE EVALUACIONES\n")
        print("6 - Generar carpetas de una evaluación")
        print("7 - Actualizar entregas de alumnos vía mail\n\n")

        print("8 - Salir\n")

        opcion = ingresar_opcion_int(8)

        if opcion == 1:
            listar_archivos_carpeta_actual()
        elif opcion == 2:
            crear_archivo()
        elif opcion == 3:
            subir_archivo()
        elif opcion == 4:
            descargar_archivo()
        elif opcion == 5:
            sincronizar()
        elif opcion == 6:
            generar_carpetas_evaluacion()
        elif opcion == 7:
            actualizar_entregas_alumnos()
        elif opcion == 8:
            continuar_en_menu = False


def main() -> None:
    # ¡Próximamente, más funcionalidades!
    menu()
        

main()
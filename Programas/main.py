# TRABAJO PRÁCTICO N°2 DE ALGORITMOS Y PROGRAMACIÓN I

import archivos
import carpetas
import drive
import gmail


def ingresar_opcion_int(rango_opciones: int) -> int:
    opcion = input(">>> Ingrese la opción:   ")
    while not (opcion.isnumeric() and 0 < int(opcion) <= rango_opciones):
        if rango_opciones == 1:
            opcion = input("Pulse 1 >>>   ")
        else:
            opcion = input(f"Ingrese una opcion entre 1 y {rango_opciones} >>>   ")
    return int(opcion)


def listar_archivos_carpeta_actual() -> None:
    pass

def crear_archivo() -> None:
    pass

def subir_archivo() -> None:
    pass

def descargar_archivo() -> None:
    pass

def sincronizar() -> None:
    pass

def generar_carpetas_evaluacion() -> None:
    pass

def actualizar_entregas_alumnos() -> None:
    pass


def menu() -> None:
    continuar_en_menu = True

    while continuar_en_menu:
        print("GOOGLE DRIVE\n\n")
        print("1 - Listar archivos de la carpeta actual")
        print("2 - Crear un archivo")
        print("3 - Subir un archivo")
        print("4 - Descargar un archivo")
        print("5 - Sincronizar")
        print("6 - Generar carpetas de una evaluación")
        print("7 - Actualizar entregas de alumnos vía mail")
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
    # Irán más cosas en el main (supongo)
    menu()
        

main()
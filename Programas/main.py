# TRABAJO PRÁCTICO N°2 DE ALGORITMOS Y PROGRAMACIÓN I


#Librerias deL sistema
from pathlib import Path
import os
#import time


#Librerias de la aplicacion
import archivos
import carpetas
#import drive     
import gmail


#Ruta por defecto
RUTA_CARPETA = "EVALUACIONES"
RUTA_ENTREGAS_ALUMNOS = f"{Path.home()}/Desktop/{RUTA_CARPETA}"


def limpiar_pantalla() -> None:
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def validar_decision(decision: int) -> int:
    #PRE: Recibimos como entero la decision del usuario.
    #POST: Si pasa la validacion, se retorna el entero introducido por el usuario.
    
    numero_fuera_de_rango = True
    while numero_fuera_de_rango:

        if decision < 1 or decision > 8:
            decision = int(input("Esta introduciendo un valor que no esta en el rango, introduce de vuelta "))
        else:
            numero_fuera_de_rango = False
    
    return decision


def decision_usuario() -> int:
    #PRE: No recibimos ningun parametro
    #POST: Se retorna la decision del usuario como un entero.

    valor = False
    while valor == False:

        try:
            decision = int(input("\nMarque la opcion deseada:  "))
            decision_validada = validar_decision(decision)
            valor = True
        except ValueError:
            print("Estas introduciendo caracteres, debe ser un numero entero")

    return decision_validada


def generar_carpetas_evaluacion(emails_entregas_correctas: list, emails_entregas_incorrectas: list) -> None:
    #PRE: --
    #POST: Carpetas de docentes y alumnos generadas con los archivos de los alumnos dentro.

    nombres_archivos = gmail.main(emails_entregas_correctas, emails_entregas_incorrectas)

    if len(nombres_archivos) == 0:
        print("Por hoy no tenemos emails de evaluaciones!")
    else:
        nombre_evaluacion = input("Introduzca el nombre de la evaluación actual: ")
        limpiar_pantalla()

        carpetas.crear_carpetas_evaluaciones(nombres_archivos, nombre_evaluacion)
        archivos.buscar_y_descomprimir(f'{RUTA_ENTREGAS_ALUMNOS}/ENTREGAS_ALUMNOS', nombres_archivos)

        print(f"\n\n\nSe descargaron las entregas de los alumnos de la evaluación '{nombre_evaluacion}' exitosamente.")
        input("\nPresione una tecla para continuar...")
        limpiar_pantalla()


def actualizar_entregas_alumnos(emails_entregas_correctas: list, emails_entregas_incorrectas: list) -> None:
    #PRE: ---
    #POST: Mails enviados a los alumnos indicando si la entrega fue correcta o no.

    servicio = gmail.obtener_servicio()

    gmail.enviar_mails(servicio, emails_entregas_incorrectas, "Entrega fallida", 
                        "Tu padron no se encuentra en nuestra base de datos.")

    gmail.enviar_mails(servicio, emails_entregas_correctas, "Entrega exitosa", 
                        "Tu entrega se ha recibido exitosamente.")


def menu() -> None:
    #PRE:Esta funcion no recibe parametros para su ejecucion.
    #POST: No retornamos nada debido a que todas las accionalidades son funciones externas a esta.

    emails_entregas_correctas = list()
    emails_entregas_incorrectas = list()
    continuar_en_menu = True

    while continuar_en_menu:
        print("------------------- SISTEMA DE EVALUACIONES 'GAME OF WHILES' -------------------\n")

        opciones = ["Listar archivos de la carpeta actual","Crear un archivo", 
                    "Subir un archivo", "Descargar un archivo", "Sincronizar",
                    "Generar carpetas de una evaluación",
                    "Actualizar entregas de alumnos vía mail",
                    "Salir"]

        for opcion in range(len(opciones)):
            print(f"{opcion + 1}) {opciones[opcion]}")

        decision = decision_usuario()
        
        if decision == 1:
            pass
        elif decision == 2:
            pass
        elif decision == 3:
            pass
        elif decision == 4:
            pass
        elif decision == 5:
            pass
        elif decision == 6:
            generar_carpetas_evaluacion(emails_entregas_correctas, emails_entregas_incorrectas)
        elif decision == 7:
            actualizar_entregas_alumnos(emails_entregas_correctas, emails_entregas_incorrectas)
        else:
            continuar_en_menu = False

    print("chao!")


def main() -> None:
    menu()
        

main()

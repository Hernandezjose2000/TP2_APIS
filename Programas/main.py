# TRABAJO PRÁCTICO N°2 DE ALGORITMOS Y PROGRAMACIÓN I


import archivos
import carpetas
#import drive     
import gmail
from pathlib import Path
#import os
#import time


RUTA_CARPETA = "EVALUACIONES"
RUTA_ENTREGAS_ALUMNOS = f"{Path.home()}/Desktop/{RUTA_CARPETA}"


'''
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
'''


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


def menu() -> None:
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

            nombres_archivos = gmail.main(emails_entregas_correctas, emails_entregas_incorrectas)

            if len(nombres_archivos) == 0:
                print("Por hoy no tenemos emails de evaluaciones!")

            else:
                nombre_evaluacion = input("Como se llama la evaluacion: ")
                carpetas.crear_carpetas_evaluaciones(nombres_archivos, nombre_evaluacion)
                archivos.buscar_y_descomprimir(f'{RUTA_ENTREGAS_ALUMNOS}/ENTREGAS_ALUMNOS', nombres_archivos)

        elif decision == 7:
            
            servicio = gmail.obtener_servicio()
            gmail.enviar_mails(servicio, emails_entregas_incorrectas, "Entrega fallida", 
                                "Tu padron no se encuentra en nuestra base de datos.")

            gmail.enviar_mails(servicio, emails_entregas_correctas, "Entrega existosa", 
                                "Tu entrega se ha recibido exitosamente.")
                                
            emails_entregas_incorrectas = list()
            emails_entregas_correctas = list()

        else:
            continuar_en_menu = False

    print("chao!")


def main() -> None:
    # ¡Próximamente, más funcionalidades!
    menu()
        

main()


# ENTREGAS_ALUMNOS = ['107411  Hernandez, Jose', '789456  Villegas, Tomas']

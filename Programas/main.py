# TRABAJO PRÁCTICO N°2 DE ALGORITMOS Y PROGRAMACIÓN I


#Librerias del sistema
import os
from pathlib import Path
from time import sleep


#Librerias de la aplicacion
import archivos
import carpetas   
import gmail
import drive 


#Ruta por defecto
RUTA_CARPETA = "EVALUACIONES"
RUTA_ENTREGAS_ALUMNOS = f"{Path.home()}/Desktop/{RUTA_CARPETA}"


def limpiar_pantalla() -> None:
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def validar_decision(decision: int) -> int:
    '''PRE: Recibimos como entero la decision del usuario.
    POST: Si pasa la validacion, se retorna el entero introducido por el usuario.'''
    
    numero_fuera_de_rango = True
    while numero_fuera_de_rango:

        if decision < 1 or decision > 10:
            decision = int(input("Esta introduciendo un valor que no esta en el rango, introduce de vuelta "))
        else:
            numero_fuera_de_rango = False
    
    return decision


def decision_usuario() -> int:
    '''PRE: No recibimos ningun parametro
    POST: Se retorna la decision del usuario como un entero.'''

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
    '''PRE: --
    POST: Carpetas de docentes y alumnos generadas con los archivos de los alumnos dentro.'''

    nombres_archivos = gmail.main(emails_entregas_correctas, emails_entregas_incorrectas)

    if len(nombres_archivos) == 0:
        print("Por hoy no tenemos emails de evaluaciones!")
    else:
        nombre_evaluacion = input("\n>>>>> Introduzca el nombre de la evaluación actual: ")
        carpetas.crear_carpetas_evaluaciones(nombres_archivos, nombre_evaluacion)

        print("Descomprimiendo archivos de los alumnos...\n\n")
        sleep(1.5)
        archivos.buscar_y_descomprimir(f'{RUTA_ENTREGAS_ALUMNOS}/ENTREGAS_ALUMNOS', nombres_archivos)
        print(f"\n\n\n>>>>> Se descargaron las entregas de los alumnos de la evaluación '{nombre_evaluacion}' exitosamente. ")

        entregas = os.path.normpath(f'{RUTA_ENTREGAS_ALUMNOS}\{nombre_evaluacion}')
        print(f">>>>> Los archivos se encuentran en: {entregas}\n")
        input("Presione ENTER para continuar ")

        limpiar_pantalla()
        sleep(0.3)


def actualizar_entregas_alumnos(emails_entregas_correctas: list, emails_entregas_incorrectas: list) -> None:
    '''PRE: ---
    POST: Mails enviados a los alumnos indicando si la entrega fue correcta o no.'''

    servicio = gmail.obtener_servicio()

    gmail.enviar_mails(servicio, emails_entregas_incorrectas, "Entrega fallida", 
                        "Tu padron no se encuentra en nuestra base de datos.")

    gmail.enviar_mails(servicio, emails_entregas_correctas, "Entrega exitosa", 
                        "Tu entrega se ha recibido exitosamente.")


def menu() -> None:
    '''PRE:Esta funcion no recibe parametros para su ejecucion.
    POST: No retornamos nada debido a que todas las accionalidades son funciones externas a esta.'''

    servicio = drive.obtener_servicio()
    emails_entregas_correctas = list()
    emails_entregas_incorrectas = list()
    continuar_en_menu = True

    while continuar_en_menu:
        print("\n------------------- SISTEMA DE EVALUACIONES 'GAME OF WHILES' -------------------\n")

        opciones = ["Listar archivos de la carpeta actual","Crear un archivo", 
                    "Subir un archivo al Drive", "Descargar un archivo desde Drive","Listar archivos en Drive",
                    "Mover archivos en Drive","Sincronizar local y remoto","Generar carpetas de una evaluación",
                    "Actualizar entregas de alumnos vía mail","Salir"]

        for opcion in range(len(opciones)):
            print(f"{opcion + 1}) {opciones[opcion]}")

        decision = decision_usuario()
        
        if decision == 1:
            pass

        elif decision == 2: #preguntar si desea crear en Drive, si la respuesta es si, llama a drive.opcion_subir
            pass

        elif decision == 3:
           drive.opcion_subir(servicio)

        elif decision == 4:
           drive.descargar_archivo(servicio) #falta binario aun
  
        elif decision == 5:
            drive.opcion_listar(servicio)

        elif decision == 6:
            drive.mover_archivo(servicio)

        elif decision == 7: #SINCRONIZACION
            pass    

        elif decision == 8:
            generar_carpetas_evaluacion(emails_entregas_correctas, emails_entregas_incorrectas)

        elif decision == 9:
            actualizar_entregas_alumnos(emails_entregas_correctas, emails_entregas_incorrectas)

        else:
            continuar_en_menu = False

    print("chao!")


def main() -> None:
    menu()
        

main()


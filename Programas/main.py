# TRABAJO PRÁCTICO N°2 DE ALGORITMOS Y PROGRAMACIÓN I


import archivos
import carpetas
#import drive     
import gmail
#import os
#import time
from pathlib import Path


RUTA_CARPETA = "EVALUACIONES"
RUTA_ENTREGAS_ALUMNOS = f"{Path.home()}/Desktop/{RUTA_CARPETA}"


'''
    Python ejecuta los archivos al importarlos, así que hay que colocar los client_secret en la misma carpeta que main.py,
    o el programa no va a funcar porque no los encuentra
'''

'''
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
'''


def validar_decision(decision:int) -> int:
    #PRE: Recibimos como entero la decision del usuario.
    #POST: Si pasa la validacion, se retorna el entero introducido por el usuario.
    
    numero_fuera_de_rango = True
    while numero_fuera_de_rango:

        if decision < 1 or decision > 8:
            decision = int(input("Esta introduciendo un valor que no esta en el rango, introduce de vuelta "))
        else:
            numero_fuera_de_rango = False
    
    return decision


def decision_usuario() ->int:
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
                #archivos.buscar_y_descomprimir(f'{RUTA_ENTREGAS_ALUMNOS}/ENTREGAS_ALUMNOS', nombres_archivos)

                '''
                entregaron = nombres_archivos
                no_entregaron = carpetas.crear_carpetas_evaluaciones(nombres_archivos, nombre_evaluacion)

                if input("¿Desea ver quienes entregaron hasta ahora y quiénes no? (s/n):  ").lower() = "s":
                    carpetas.mostrar_entregas(entregaron, no_entregaron)
                '''

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

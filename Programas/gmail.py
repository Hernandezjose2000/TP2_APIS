#MODULOS PROPIOS DE PYTHON
import os
import datetime
import time
import csv

#modulos para la API
from googleapiclient.discovery import Resource, build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

# Archivo generado para la API
ARCHIVO_SECRET_CLIENT = 'client_secret_gmail.json'


def cargar_credenciales() -> Credentials:
    credencial = None

    if os.path.exists('token.json'):
        with open('token.json', 'r'):
            credencial = Credentials.from_authorized_user_file('token.json', SCOPES)

    return credencial


def guardar_credenciales(credencial: Credentials) -> None:
    with open('token.json', 'w') as token:
        token.write(credencial.to_json())


def son_credenciales_invalidas(credencial: Credentials) -> bool:
    return not credencial or not credencial.valid


def son_credenciales_expiradas(credencial: Credentials) -> bool:
    return credencial and credencial.expired and credencial.refresh_token


def autorizar_credenciales() -> Credentials:
    flow = InstalledAppFlow.from_client_secrets_file(ARCHIVO_SECRET_CLIENT, SCOPES)

    return flow.run_local_server(open_browser=False, port=0)


def generar_credenciales() -> Credentials:
    credencial = cargar_credenciales()

    if son_credenciales_invalidas(credencial):

        if son_credenciales_expiradas(credencial):
            credencial.refresh(Request())

        else:
            credencial = autorizar_credenciales()

        guardar_credenciales(credencial)

    return credencial


def obtener_servicio() -> Resource:
    """
    Creador de la conexion a la API Gmail
    """
    return build('gmail', 'v1', credentials=generar_credenciales())

'''
Todo lo anterior a la variable servicio se encuentra en el archivo conexion_gmail, se debe importar, pero
estoy teniendo problemas para importarlos, no me reconoce la ruta, lo solucionare.
'''
ASUNTO = 19
EMAIL = 1
ARCHIVO_ADJUNTO = 1


def obteniendo_datos_mails(id_mails:list, servicio:Resource) -> dict:

    datos_emails = {} #Los almacenamos de esta manera ['28345234, TP_1', '789101112, Parcial_2', '123456, Parcial_2_Recuperatorio_1']

    for id_mail in id_mails:

        lectura_mail = servicio.users().messages().get(userId='evaluaciontp2@gmail.com', id = id_mail).execute()
        obteniendo_origen = lectura_mail['payload']['headers'][16]['value'].split("<")
        email_origen = obteniendo_origen[EMAIL].rstrip(">")
        asunto = lectura_mail['payload']['headers'][ASUNTO]['value'].split("-")
        id_archivo_adjunto = lectura_mail['payload']['parts'][ARCHIVO_ADJUNTO]['body']['attachmentId']

        datos_emails[id_mail] = {"asunto":asunto, "origen": email_origen, "adj_id":id_archivo_adjunto}
    return datos_emails



def obteniendo_ids_mails(servicio:Resource, fecha_actual:float) -> list:

    #PRE: No recibimos ningun parametro.
    #POST: Retronamos en una lista los id's de los mails.
    
    id_mails = [] #Se guaradaran asi ['123345', 'dhgfgh34534543']
    emails_recibidos = servicio.users().messages().list(userId='evaluaciontp2@gmail.com', q=f'newer: {fecha_actual}').execute()#captar la excepcion de la no conexion al servicio
    obteniendo_ids = emails_recibidos['messages']
    
    for id in obteniendo_ids:

        id_mails.append(id['id'])

    return id_mails


def obteniendo_fecha_actual() -> int:

    #PRE: No recibimos nada como argumento
    #POST: Retornamos la fecha casteada como int en formato UNIX

    fecha = str(datetime.date.today())
    conversion_unix = int(time.mktime(datetime.datetime.strptime(fecha.replace("-","/"), '%Y/%m/%d').timetuple()))

    return conversion_unix


def validando_datos_asuntos(id_mails:list, datos_emails:dict):

    lineas = []
    emails_entregas_incorrectas = []
    entregas_correctas = []

    with open("\\Users\\joseh\\Documents\\algoritmos_y_programacion_1\\TP2_APIS\\Programas\\alumnos.csv", "r") as archivo:

        lectura = csv.reader(archivo, delimiter=';')
        next(lectura)

        for linea in lectura:
            lineas.append(linea)               

        for j in id_mails:

            k = 0
            while k < 17: 
                if datos_emails[j]['asunto'][0].strip(" ") in lineas[k][1]:
                    entregas_correctas.append(datos_emails[j]['adj_id'])
                    k = 17
                else:
                    
                    if k < 16:
                        print("validando")
                    else:
                        emails_entregas_incorrectas.append(datos_emails[j]['origen'])
                    k+=1
        print(emails_entregas_incorrectas)
    
    return emails_entregas_incorrectas

def enviando_mail_entregas_fallidas(servicio:Resource, entregas_incorrectas:list):


    for mail in entregas_incorrectas:

        mensaje_email ="Por favor valida tu Padron debido a que no coincide con lo que tenemos en nuestra base de datos"
        mimeMessage = MIMEMultipart()
        mimeMessage["to"] = mail
        mimeMessage["subject"] = "Entrega de evaluacion"  
        mimeMessage.attach(MIMEText(mensaje_email, "plain"))
        decodificando_mensaje = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        mensaje = servicio.users().messages().send(userId = "evaluaciontp2@gmail.com", body = {"raw": decodificando_mensaje}).execute()


def main():

    fecha = obteniendo_fecha_actual()    
    servicio = obtener_servicio()
    id_mails = obteniendo_ids_mails(servicio, fecha)
    datos_emails = obteniendo_datos_mails(id_mails, servicio)
    emails_entregas_incorrectas = validando_datos_asuntos(id_mails, datos_emails)
    enviando_mail_entregas_fallidas(servicio, emails_entregas_incorrectas)

main()

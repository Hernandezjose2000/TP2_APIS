import os, io
import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import GOOGLE_API_USE_MTLS_ENDPOINT, build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload 

SCOPES = ['https://www.googleapis.com/auth/drive']

#Archivo generado para la api
ARCHIVO_SECRET_CLIENT = 'client_secret_drive.json'

PERMISOS = ['https://www.googleapis.com/auth/drive']

API_NAME = 'drive'

API_VERSION = 'v3'

PATH_TOKEN = 'token_drive.json'

def cargar_credenciales() -> Credentials:
    credencial = None

    if os.path.exists(PATH_TOKEN):
        with open(PATH_TOKEN, 'r'):
            credencial = Credentials.from_authorized_user_file(PATH_TOKEN, SCOPES)

    return credencial


def guardar_credenciales(credencial: Credentials) -> None:
    with open(PATH_TOKEN, 'w') as token:
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
    Creador de la conexion a la api drive.

    :return: service
    """
    return build(API_NAME, API_VERSION, credentials=generar_credenciales())



#-----------------------programa----------------------------------
#Disculpen que está desprolijo, cuando todo funcione bien arreglaré el formato

'''
Por el momento funciona todo de forma independiente, más adelante agrego si se quiere guardar en una carpeta el archivo o si queres mover 
archivos entre carpetas.
Por ahora es pura prueba y error, empirismo puro!
'''

def subir_archivo(servicio): #Sube un archivo al drive sin meterlo en alguna carpeta
    
    nombre_archivo = input('Ingrese el nombre del archivo junto con su extension (ej - imagengatito.png): ')
    ruta_archivo = input('repita el paso anterior: ') #Lo tengo que optimizar, funciona si metes 2 veces el nombre y extension.
    tipo_archivo = input ('Ingrese el tipo de archivo (ej- image/png): ')

    archivo_metadata = {'name': nombre_archivo}

    media = MediaFileUpload(ruta_archivo,  mimetype=tipo_archivo)
    archivo = servicio.files().create(body = archivo_metadata, media_body=media, fields='id').execute()

    print('ID Archivo: %s' % archivo.get('id')) 


def descargar_archivo (servicio): #aun no funciona correctamente. está copiado directamente de Google for Developers
    
    nombre_archivo = input('Ingrese el nombre del archivo: ')
   
    request = servicio.files().get_media(fileId=nombre_archivo)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = True
    while not done: #placeholder
     status, done = downloader.next_chunk()

     print ("Download %d%%.") % int(status.progress() * 100)


def crear_carpeta(servicio): #funciona! Voy a ver de crear una carpeta y a su vez crear archivo en dicha carpeta
    nombre = input('Ingrese nombre de la carpeta a crear: ')
    carpeta_metadata = {
    'name': nombre,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = servicio.files().create(body=carpeta_metadata, fields='id').execute()
    print ('ID Carpeta: %s' % file.get('id'))






def main():
    servicio = obtener_servicio()   
    crear_carpeta(servicio)


main()

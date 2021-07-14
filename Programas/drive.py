import os, io
import os.path

 
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import GOOGLE_API_USE_MTLS_ENDPOINT, build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload 
from google.auth.transport.requests import Request



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
Falta cosas como las busquedas anidadas y pasar a binario. Falta poquito!
Le voy a agregar mas detalles
'''

def subir_archivo(servicio): #Sube un archivo al drive sin meterlo en alguna carpeta
    nombre_archivo = input('Ingrese el nombre del archivo junto con su extension (ej - imagengatito.png): ')
    ruta_archivo = input('Ingrese donde se encuentra el archivo (ruta completa): ')
    tipo_archivo = input ('Ingrese el tipo de archivo (ej- image/png): ')

    archivo_metadata = {'name': nombre_archivo}

    media = MediaFileUpload(ruta_archivo,  mimetype=tipo_archivo)
    archivo = servicio.files().create(body = archivo_metadata, media_body=media, fields='id').execute()

    print('ID Archivo: %s' % archivo.get('id')) 



def crear_carpeta(servicio): #carpeta vacia
    nombre = input('Ingrese nombre de la carpeta a crear: ')
    carpeta_metadata = {
    'name': nombre,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = servicio.files().create(body=carpeta_metadata, fields='id').execute()
    print ('ID Carpeta: %s' % file.get('id'))


def crear_archivo_vacio(servicio): #Crea un archivo sin contenido y sin extension
    nombre_nuevo_archivo = input('Ingrese el nombre del archivo a crear: ')
    file_metadata = {
    'name' : nombre_nuevo_archivo,
    'mimeType' : 'application/vnd.google-apps.drive-sdk'
    }
    file = servicio.files().create(body=file_metadata,
                                    fields='id').execute()
    print ('ID archivo: %s' % file.get('id'))


def crear_archivo(servicio):
    pass



def listar_archivos(servicio): 
    listar = servicio.files().list(
        pageSize=5, fields="nextPageToken, files(id, name, mimeType, parents)").execute()
    items = listar.get('files', [])

    if not items:
        print('No se encontraron archivos.')
    else:
        rows = []
        for item in items:

            id = item["id"]
            name = item["name"]
            try:
              parents = item["parents"]
            except:
              parents = "N/A"

            mime_type = item["mimeType"]
  
            rows.append((id, name, parents, mime_type))
        print("Archivos:")
        print(items) #Lo voy a poner mas legible! 






def descargar_archivo(servicio): #falta pasar a binario!
    id_archivo = input('ID del archivo: ')
    ruta_archivo = input ('¿Dónde lo desea guardar? (ruta completa): ')
    request = servicio.files().get_media(fileId=id_archivo)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(ruta_archivo,'wb') as f:
        fh.seek(0)
        f.write(fh.read())



def mover_archivo(servicio):
    pass




def main():
    servicio = obtener_servicio()
    listar_archivos(servicio)
    
    
    


main()

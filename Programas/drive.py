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

    
#----------------TP2-APIS-FUNCIONALIDAD_DRIVE------------------

TIPO_ARCHIVOS = ['text/x-python-script',
'video/mp4',
'text/txt',
'text/plain',
'text/csv',
'image/png',
'image/jpg']


def subir_archivo(servicio:Resource, ruta_archivo) -> None:  
    '''
    PRE: Recibe datos del archivo que se desea subir. 
    POST: Sube el archivo al drive y le muestra al usuario la ID del mismo. No se sube a ninguna carpeta.
    '''
    print (TIPO_ARCHIVOS)
    nombre_archivo = input('Ingrese el nombre del archivo junto con su extension (ej - imagengatito.png): ')
    tipo_archivo = input ('Ingrese el tipo de archivo (ej- image/png): ')
    
    archivo_metadata = {'name': nombre_archivo}

    tipo = MediaFileUpload(ruta_archivo,  mimetype=tipo_archivo)
    archivo = servicio.files().create(body = archivo_metadata, media_body=tipo, fields='id').execute()

    print('Archivo subido con éxito. \n ID Archivo: %s' % archivo.get('id')) 


def crear_carpeta(servicio:Resource) -> None: 
    '''
    PRE: Recibe datos de la carpeta que se desea crear. 
    POST: Crea la carpeta en 'Mi Unidad' en Drive. Muestra la ID de la carpeta
    '''
    nombre = input('Ingrese nombre de la carpeta a crear: ')
    carpeta_metadata = {
    'name': nombre,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = servicio.files().create(body=carpeta_metadata, fields='id').execute()
    print ('Carpeta creada con éxito. \n ID Carpeta: %s' % file.get('id'))


def crear_archivo_vacio(servicio:Resource) -> None:
    '''
    PRE: Pide el nombre del archivo a crear
    POST: Crea el archivo en 'Mi Unidad' en Drive. El mismo es vacío, no tiene extensión ni contenido.
    '''
    nombre_nuevo_archivo = input('Ingrese el nombre del archivo a crear: ')
    nuevo_archivo_metadata = {
    'name' : nombre_nuevo_archivo,
    'mimeType' : 'application/vnd.google-apps.drive-sdk'
    }
    crear = servicio.files().create(body=nuevo_archivo_metadata, fields='id').execute()
    print ('Archivo creado con éxito. \n ID archivo: %s' % crear.get('id'))


def listar_archivos_en_carpetas(servicio:Resource) -> None: #busquedas anidadas
    '''
    PRE: Pide el ID de la carpeta en dondr se desean ver los archivos.
    POST: Imprime todos los archivos en esa carpeta.
    '''
    id_carpeta_a_listar = input('Ingrese el ID de la carpeta donde quiera ver los archivos: ')
    query = (f'parents = "{id_carpeta_a_listar}"')
    respuesta = servicio.files().list(q=query).execute()
    archivos = respuesta.get('files')
    nextPageToken = respuesta.get('nextPageToken')
    
    while nextPageToken:
        response = servicio.files().list(q=query, pageToken=nextPageToken).execute()
        archivos.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    print (archivos)


def descargar_archivo(servicio:Resource, ruta_archivo_descargado) -> None: #falta pasar a binario!
    '''
    PRE:
    POST: 
    '''
    listar_archivos(servicio)
    n = int (input('¿Cuántos archivos quiere descagar? '))
    for i in range (n):
       id_archivo = input('ID del archivo: ')
       
    
       request = servicio.files().get_media(fileId=id_archivo)
       fh = io.BytesIO()
       descarga = MediaIoBaseDownload(fh, request)
       done = False
       while done is False:
            status, done = descarga.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
       with io.open(ruta_archivo_descargado,'wb') as f:
            fh.seek(0)
            f.write(fh.read())


def listar_archivos(servicio:Resource, size = 20) -> None:
    '''
    PRE: Verifica si hay algun archivo en TODO el drive
    POST: Muestra TODOS los archivos en el Drive, incluso en la papelera. Muestra ID, nombre, tipo de archivo y dónde se encuentra.
    '''
    listar = servicio.files().list(
         pageSize=size,fields="nextPageToken, files(id, name, mimeType, parents)").execute()
    archivos = listar.get('files', [])

    if not archivos:
        print('No se encontraron archivos.')
    else:  
        print("Archivos:\n")
        for archivo in archivos:
            if archivo['mimeType'] != "application/vnd.google-apps.folder":
                print (" ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>10} | Carpeta Contenedora: {3} \n".format(archivo['id'], archivo['name'], archivo['mimeType'], archivo['parents']))


def listar_carpetas(servicio: Resource, size = 30):
    '''
    PRE: Analiza el tipo de archivo de todos los archivos en el drive
    POST: Imprime por pantalla el ID, Nombre y tipo de archivo de las carpetas. 
    '''

    listar = servicio.files().list(
         pageSize=size,fields="nextPageToken, files(id, name, mimeType)").execute()
    carpetas_aux = listar.get('files', [])
    carpetas = list()
    
    for i in range(len(carpetas_aux)):
            if carpetas_aux[i]['mimeType'] == "application/vnd.google-apps.folder":
                carpetas.append(carpetas_aux[i])
        
    for carpeta in carpetas:
        print (" ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>15} \n".format(carpeta['id'], carpeta['name'], carpeta['mimeType']))


def mover_archivo(servicio:Resource) -> None:
    '''
    PRE: Pide la ID del archivo a mover y la ID de la nueva carpeta contenedora.
    POST: Mueve el archivo
    '''
    listar_archivos(servicio)
    id_archivo_mover = input('Ingrese la ID del archivo que desea mover: ')
    listar_carpetas(servicio)
    nueva_carpeta_contenedora = input('Ingrese la ID de la carpte que desea usar: ')

    # Localiza la carpeta contenedora y saca el archivo
    file = servicio.files().get(fileId=id_archivo_mover, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))

    # Mueve el archivo a la nueva carpeta
    file = servicio.files().update(
        fileId=id_archivo_mover,
        addParents=nueva_carpeta_contenedora,
        removeParents=previous_parents,
        fields=('id, parents')
    ).execute()


def main() -> None:
    servicio = obtener_servicio()
    #agreguen la funcion que quieran probar
    


main()

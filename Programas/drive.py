import os, io
import os.path
import shutil

 
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
'image/jpeg']



def subir_archivo(servicio:Resource) -> None:  
    '''
    PRE: Recibe datos del archivo que se desea subir. 
    POST: Sube el archivo al drive y le muestra al usuario la ID del mismo. No se sube a ninguna carpeta.
    '''
    print('\nEstos son los tipos de archivo generalmente usados:')
    for tipo in TIPO_ARCHIVOS:
        print (tipo)

    nombre_archivo = input('\nIngrese el nombre del archivo junto con su extension (ej - imagen.png): ')
    tipo_archivo = input ('\nIngrese el tipo de archivo (ej- image/png): ')
    archivo_metadata = {
        "name": nombre_archivo
    }
    
    subida = MediaFileUpload(nombre_archivo, tipo_archivo, resumable=True)
    archivo = servicio.files().create(body=archivo_metadata, media_body=subida, fields='id').execute()
    print("\nArchivo subido con éxito. \n ID Archivo: ", archivo.get("id"))


def subir_archivo_crear_carpeta(servicio:Resource) -> None:
    '''
    PRE: Recibe datos del archivo que se desea subir. Recibe datos de la carpeta a crear.
    POST: Sube el archivo a la nueva carpeta y le muestra al usuario la ID de los mismos. 
    '''
    nombre = input('\nIngrese nombre de la carpeta a crear: ')
    carpeta_metadata = {
    'name': nombre,
    'mimeType': 'application/vnd.google-apps.folder'
    }

    carpeta = servicio.files().create(body=carpeta_metadata, fields="id").execute()
    id_carpeta = carpeta.get("id")

    print("\nCarpeta creada con éxito. \n ID Carpeta: ", id_carpeta) 
    nombre_archivo = input('\nIngrese el nombre del archivo junto con su extension (ej - imagen.png): ')

    archivo_metadata = {
        "name": nombre_archivo,
        "parents": [id_carpeta]
    }
    
    subida = MediaFileUpload(nombre_archivo, resumable=True)
    archivo = servicio.files().create(body=archivo_metadata, media_body=subida, fields='id').execute()
    print("\nArchivo subido con éxito. \n ID Archivo: ", archivo.get("id"))


def descargar_archivo(servicio):
    '''
    PRE: Pregunta cuántos archivos se desea descargar y el nombre con el que se lo desea guardar
    POST: Descargar el archivo con el nombre deseado
    '''
    listar_archivos(servicio)
    archivo = input("Ingrese el nombre del archivo que desea descargar:  ")
    ruta_preferida = input("Ingrese la ruta de descarga:  ")
    ruta = f'{ruta_preferida}/{archivo}'
    descargar_archivo_2(servicio, ruta)


def descargar_archivo_2(service, filePath):
    # Note: The parent folders in filePath must exist
    fileId = input('\nID del archivo: ')
    print("-> Downloading file with id: {0} name: {1}".format(fileId, filePath))
    request = service.files().get_media(fileId=fileId)
    fh = io.FileIO(filePath, mode='wb')

    try:
        downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024)

        done = False
        while done is False:
            status, done = downloader.next_chunk(num_retries = 2)
            if status:
                print("Download %d%%." % int(status.progress() * 100))
        print("Download Complete!")
    finally:
        fh.close()


def listar_archivos_en_carpetas(servicio:Resource) -> None: #busquedas anidadas
    '''
    PRE: Pide el ID de la carpeta en dondr se desean ver los archivos.
    POST: Imprime todos los archivos en esa carpeta.
    '''
    listar_carpetas(servicio)

    id_carpeta_a_listar = input('\nIngrese el ID de la carpeta donde quiera ver los archivos: ')
    query = (f'parents = "{id_carpeta_a_listar}"')
    respuesta = servicio.files().list(q=query).execute()
    archivos = respuesta.get('files', [])
    nextPageToken = respuesta.get('nextPageToken')
    
    while nextPageToken:
        response = servicio.files().list(q=query, pageToken=nextPageToken).execute()
        archivos.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    
    if not archivos:
        print('No se encontraron archivos.')

    else:  
        print("Archivos:\n")
        for archivo in archivos:  
               print (" ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>10} \n".format(archivo['id'], archivo['name'], archivo['mimeType']))


def listar_archivos(servicio:Resource, size = 8) -> None:
    '''
    PRE: Verifica si hay algun archivo en TODO el drive
    POST: Muestra hasta 20 archivos de todo el Drive, incluso en la papelera. Muestra ID, nombre, tipo de archivo y dónde se encuentra.
    '''

    listar = servicio.files().list(
             pageSize=size,
             fields="nextPageToken, files(id, name, mimeType, parents)"
             ).execute()

    archivos = listar.get('files', [])

    if not archivos:
        print('\nNo se encontraron archivos.')
    else:  
        print("\nArchivos:\n")

        for archivo in archivos:
              print (" ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>10} | Carpeta Contenedora: {3} \n".format(archivo['id'], archivo['name'], archivo['mimeType'], archivo['parents']))


def listar_archivos_segun_tipo(servicio:Resource, size = 20) -> None:
    '''
    PRE: Busca los archivos en todo el drive segun el tipo de archivo ingresado
    POST: Imprime por pantalla una lista con archivos de ese tipo.
    '''
    print('\nEstos son los tipos de archivo generalmente usados:')
    for tipo in TIPO_ARCHIVOS:
        print (tipo)

    mimetype = input('\nIngrese el tipo de archivo: ')

    listar = servicio.files().list(
             pageSize=size,
             fields="nextPageToken, files(id, name, mimeType, parents)"
             ).execute()

    archivos = listar.get('files', [])

    if not archivos:
        print('\nNo se encontraron archivos.')
    else:  
        print("\nArchivos:\n")
        for archivo in archivos:

            if archivo['mimeType'] == mimetype:
                    print (" ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>10} | Carpeta Contenedora: {3} \n".format(archivo['id'], archivo['name'], archivo['mimeType'], archivo['parents']))


def listar_carpetas(servicio: Resource, size = 20):
    '''
    PRE: Analiza el tipo de archivo de todos los archivos en el drive
    POST: Imprime por pantalla el ID, Nombre y tipo de archivo de las carpetas. 
    '''

    listar = servicio.files().list(
             pageSize=size,
             fields="nextPageToken, files(id, name, mimeType)"
             ).execute()

    carpetas_aux = listar.get('files', [])
    carpetas = list()
    
    for i in range(len(carpetas_aux)):
            if carpetas_aux[i]['mimeType'] == "application/vnd.google-apps.folder":
                carpetas.append(carpetas_aux[i])
        
    for carpeta in carpetas:
        print (" ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>15} \n".format(carpeta['id'], carpeta['name'], carpeta['mimeType']))


def listar (servicio):
    print('''\n¿Que desea hacer? 
        1.Listar TODOS los archivos y carpetas
        2.Listar carpetas
        3.Listar archivos en una carpeta
        4.Listar archivos según su tipo ''')
    opcion = int(input('\nIngrese una opcion: '))
    if opcion == 1:
        listar_archivos(servicio)
    elif opcion == 2:
        listar_carpetas(servicio)
    elif opcion == 3:
        listar_archivos_en_carpetas(servicio)
    elif opcion == 4:
        listar_archivos_segun_tipo(servicio)
  

def mover_archivo(servicio:Resource) -> None:
    '''
    PRE: Pide la ID del archivo a mover y la ID de la nueva carpeta contenedora.
    POST: Mueve el archivo
    '''
    listar_archivos(servicio)
    id_archivo_mover = input('\nIngrese la ID del archivo que desea mover: ')
    listar_carpetas(servicio)
    nueva_carpeta_contenedora = input('\nIngrese la ID de la carpte que desea usar: ')

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
    #descargar_archivo(servicio)


main()

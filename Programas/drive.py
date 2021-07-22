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
'image/jpeg',
'application/pdf',
'application/vnd.google-apps.file',
'application/vnd.google-apps.document',
'application/vnd.google-apps.spreadsheet']



def subir_archivo(servicio:Resource) -> None:  
    '''
    PRE: Recibe datos del archivo que se desea subir. 
    POST: Sube el archivo al drive y le muestra al usuario la ID del mismo. No se sube a ninguna carpeta.
    '''
    
    ruta_archivo = input("\nIngrese la ruta del archivo COMPLETA (Agregue el nombre con extension al final):  ")
    nombre_archivo = input('\nIngrese el nombre con el que desea guardar el archivo junto con su extensión: ')
    
    archivo_metadata = {
        "name": nombre_archivo
    }
    
    subida = MediaFileUpload(ruta_archivo, resumable=True)
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
    ruta_archivo = input("\nIngrese la ruta del archivo COMPLETA (Agregue el nombre con extension al final):  ")
    nombre_archivo = input('\nIngrese el nombre con el que desea guardar el archivo: ')
    
    archivo_metadata = {
        "name": nombre_archivo,
        "parents": [id_carpeta]
    }
    
    subida = MediaFileUpload(ruta_archivo, resumable=True)
    archivo = servicio.files().create(body=archivo_metadata, media_body=subida, fields='id').execute()

    print("\nArchivo subido con éxito. \n ID Archivo: ", archivo.get("id"))



def opcion_subir(servicio:Resource) -> None:
    '''
    PRE: Le pregunta al usuario dónde desea guardar el archivo a subir.
    POST: Sube el archivo según la opción elegida.
    '''
    print('''\n¿Que desea hacer? 
    1.Subir archivo a "Mi Unidad"
    2.Crear una carpeta y subir archivo a la carpeta.
    ''')
    opcion = int(input('\nIngrese una opcion: '))

    if opcion == 1:
        subir_archivo(servicio)
    elif opcion == 2:
        subir_archivo_crear_carpeta(servicio)

    

def descargar_archivo(servicio: Resource) -> None:
    '''
    PRE: Pregunta los datos del archivo que se desea descargar, entre ellos la ruta.
    POST: Recibe la función de descarga.
    '''

    listar_archivos(servicio)
    archivo = input("\nIngrese el nombre del archivo que desea descargar junto con su extensión:  ")
    ruta_preferida = input("\nIngrese la ruta de descarga:  ")
    ruta = f'{ruta_preferida}/{archivo}'
    descargar_archivo_2(servicio, ruta)



def descargar_archivo_2(servicio: Resource, ruta: str) -> None:
    '''
    PRE: ~
    POST: Descarga el archivo.
    '''

    Id_archivo_descargar = input('\nIngrese el ID del archivo: ')
    print("\n-> Descargando el archivo - id: {0} nombre: {1}".format(Id_archivo_descargar, ruta))
    
    solicitud = servicio.files().get_media(fileId = Id_archivo_descargar)
    fh = io.FileIO(ruta, mode='wb')
      
    try:
        descarga = MediaIoBaseDownload(fh, solicitud, chunksize = 1024*1024)

        terminar = False
        while terminar is False:
            estado, terminar = descarga.next_chunk(num_retries = 2)
            if estado:
                print("\nDescarga %d%%." % int(estado.progress() * 100))
        print("\n¡Archivo descargado con éxito!")    
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
        print('\nNo se encontraron archivos.')

    else:  
        print("\nArchivos:\n")

        for i in range(len(archivos)):  
            print(f"{archivos[i]['id']}  |  {archivos[i]['name']}  |  {archivos[i]['mimeType']}")
            print ('_' * 175)


def listar_archivos(servicio:Resource, size = 20) -> None:
    '''
    PRE: Verifica si hay algun archivo en TODO el drive
    POST: Muestra hasta 20 archivos de todo el Drive, incluso en la papelera. Muestra ID, nombre, tipo de archivo y dónde se encuentra.
    '''

    listar = servicio.files().list(
             pageSize=size,
             fields="nextPageToken, files(id, name, mimeType, parents, modifiedTime)"
             ).execute()

    archivos = listar.get('files', [])

    if not archivos:
        print('\nNo se encontraron archivos.')
    else:  
        print("\nArchivos:\n")

        for archivo in archivos:
            try:
              print ("\n ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>10} | Carpeta Contenedora: {3} | Última Modificación: {4} \n".format(archivo['id'], archivo['name'], 
              archivo['mimeType'], archivo['parents'], archivo['modifiedTime']))
              print ('_' * 175)
            except Exception:
                pass



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
                   



def listar_carpetas(servicio: Resource, size = 20) ->None:
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

    if not carpetas_aux:
        print ('\nNo se encontraron carpetas')
    
    else:
        for i in range(len(carpetas_aux)):
            if carpetas_aux[i]['mimeType'] == "application/vnd.google-apps.folder":
                carpetas.append(carpetas_aux[i])
        
        for carpeta in carpetas:
            print (" ID: {0:<20} | Nombre: {1:>5} | Tipo de Archivo: {2:>15} \n".format(carpeta['id'], carpeta['name'], carpeta['mimeType']))



def opcion_listar (servicio:Resource) -> None:
    '''
    PRE: Le da al usuario varias opciones para listar y buscar archivos.
    POST: Segun la opcion, lista archivos/carpetas con diferentes filtros.
    '''

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
    POST: Mueve el archivo.
    '''
    listar_archivos(servicio)
    id_archivo_mover = input('\nIngrese la ID del archivo que desea mover: ')
    listar_carpetas(servicio)
    nueva_carpeta_contenedora = input('\nIngrese la ID de la carpte que desea usar: ')

    # Localiza la carpeta contenedora y saca el archivo
    archivo_mover = servicio.files().get(fileId=id_archivo_mover, fields='parents').execute()
    anterior_directorio = ",".join(archivo_mover.get('parents'))

    # Mueve el archivo a la nueva carpeta
    archivo_mover = servicio.files().update(
        fileId=id_archivo_mover,
        addParents=nueva_carpeta_contenedora,
        removeParents=anterior_directorio,
        fields=('id, parents')
    ).execute()
    print ('\n El archivo se movió con éxito.')



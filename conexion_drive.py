import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
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
obtener_servicio()
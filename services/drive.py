"""
Funciones para trabajar con Google Drive y Google Sheets usando
una cuenta de servicio. Permite subir archivos y leer datos de hojas.
"""
from pathlib import Path
import os, io, logging, json
from fastapi import HTTPException
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

"""
Crea y devuelve un cliente de Google Drive usando credenciales
de una cuenta de servicio (service account).
"""
def _get_drive_service():
    # Intentamos obtener las credenciales desde una variable de entorno como JSON.
    json_creds = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if json_creds:
        try:
            # Si existen, las cargamos como diccionario.
            creds_info = json.loads(json_creds)
            # Creamos las credenciales directamente desde el JSON.
            creds = Credentials.from_service_account_info(
                creds_info,
                scopes=["https://www.googleapis.com/auth/drive.file"]
            )
            return build("drive", "v3", credentials=creds)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al leer credenciales desde entorno: {e}")

    # Si no hay JSON en variables, intentamos usar un archivo de credenciales.
    creds_path_env = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    if creds_path_env and Path(creds_path_env).exists():
        creds_path = Path(creds_path_env)
    else:
        # Si no hay ruta en variable, buscamos credentials.json dentro del proyecto.
        creds_path = Path(__file__).resolve().parents[1] / "credentials.json"
        if not creds_path.exists():
            raise HTTPException(status_code=500, detail="No se encontró credentials.json ni GOOGLE_SERVICE_ACCOUNT_FILE")

    # Cargamos credenciales desde archivo local.
    creds = Credentials.from_service_account_file(
        str(creds_path),
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build("drive", "v3", credentials=creds)

"""
Sube contenido binario (bytes) a Google Drive en la carpeta indicada.
Puede hacerlo público y devuelve varias URLs útiles del archivo.
"""
def upload_bytes_to_drive(contenido: bytes, filename: str, mime: str, folder_id: str, make_public: bool = True):
    try:
        # Obtenemos el cliente autenticado de Google Drive.
        service = _get_drive_service()
        # Definimos el nombre del archivo y la carpeta destino en Drive.
        file_metadata = {"name": filename, "parents": [folder_id]}
        # Preparamos los bytes para subirlos como un archivo.
        media = MediaIoBaseUpload(io.BytesIO(contenido), mimetype=mime, resumable=True)

        # Creamos el archivo en Drive y pedimos que regrese enlaces útiles.
        created = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink, webContentLink"
        ).execute()

        # Obtenemos el ID del archivo recién creado.
        file_id = created.get("id")

        # Si se solicita, damos permisos de lectura pública a cualquiera.
        if make_public and file_id:
            try:
                service.permissions().create(
                    fileId=file_id,
                    body={"type": "anyone", "role": "reader"}
                ).execute()
            except Exception:
                logging.exception("No se pudo aplicar permiso público (anyone:reader)")

        # URL para ver el archivo en Google Drive.
        url_view = f"https://drive.google.com/file/d/{file_id}/view" if file_id else None
        # URL para descargar directamente el archivo sin abrir Drive.
        url_download = f"https://drive.google.com/uc?id={file_id}&export=download" if file_id else None

        # Regresamos toda la información útil del archivo subido.
        return {
            "id": file_id,
            "webViewLink": created.get("webViewLink"),
            "webContentLink": created.get("webContentLink"),
            "url_view": url_view,
            "url_download": url_download,
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error subiendo a Google Drive")
        raise HTTPException(status_code=502, detail=f"Error subiendo a Google Drive: {e}")

"""
Construye un cliente autenticado para Google Sheets usando una cuenta de servicio.
Solo tiene permisos de lectura.
"""
def get_sheets_service():
    # Intentamos cargar credenciales desde variable de entorno JSON.
    json_creds = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if json_creds:
        try:
            # Construimos credenciales directamente desde datos en memoria.
            creds_info = json.loads(json_creds)
            creds = Credentials.from_service_account_info(
                creds_info,
                scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
            )
            return build("sheets", "v4", credentials=creds)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al leer credenciales desde entorno: {e}")

    # Si no existe JSON, usamos archivo físico de credenciales.
    creds_path_env = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    if creds_path_env and Path(creds_path_env).exists():
        creds_path = Path(creds_path_env)
    else:
        creds_path = Path(__file__).resolve().parents[1] / "credentials.json"
        if not creds_path.exists():
            raise HTTPException(status_code=500, detail="No se encontró credentials.json ni GOOGLE_SERVICE_ACCOUNT_FILE")

    # Construimos el cliente de Google Sheets API.
    creds = Credentials.from_service_account_file(
        str(creds_path),
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return build("sheets", "v4", credentials=creds)

"""
Lee un rango de celdas desde Google Sheets.
Input: spreadsheet_id y rango A1 (por ejemplo 'Datos!A:E').
Output: lista de filas con los valores obtenidos.
"""
def read_sheet_data(spreadsheet_id: str, range_: str):
    # Obtenemos el cliente para Google Sheets.
    sheets_service = get_sheets_service()
    sheet = sheets_service.spreadsheets()
    # Ejecutamos la petición para leer el rango solicitado.
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    # Si no hay valores, regresamos una lista vacía.
    return result.get("values", [])
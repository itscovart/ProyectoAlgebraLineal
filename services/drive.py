from pathlib import Path
import os, io, logging, json
from fastapi import HTTPException
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

def _get_drive_service():
    json_creds = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if json_creds:
        try:
            creds_info = json.loads(json_creds)
            creds = Credentials.from_service_account_info(
                creds_info,
                scopes=["https://www.googleapis.com/auth/drive.file"]
            )
            return build("drive", "v3", credentials=creds)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al leer credenciales desde entorno: {e}")

    creds_path_env = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    if creds_path_env and Path(creds_path_env).exists():
        creds_path = Path(creds_path_env)
    else:
        creds_path = Path(__file__).resolve().parents[1] / "credentials.json"
        if not creds_path.exists():
            raise HTTPException(status_code=500, detail="No se encontró credentials.json ni GOOGLE_SERVICE_ACCOUNT_FILE")

    creds = Credentials.from_service_account_file(
        str(creds_path),
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build("drive", "v3", credentials=creds)

def upload_bytes_to_drive(contenido: bytes, filename: str, mime: str, folder_id: str, make_public: bool = True):
    try:
        service = _get_drive_service()
        file_metadata = {"name": filename, "parents": [folder_id]}
        media = MediaIoBaseUpload(io.BytesIO(contenido), mimetype=mime, resumable=True)

        created = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink, webContentLink"
        ).execute()

        file_id = created.get("id")

        if make_public and file_id:
            try:
                service.permissions().create(
                    fileId=file_id,
                    body={"type": "anyone", "role": "reader"}
                ).execute()
            except Exception:
                logging.exception("No se pudo aplicar permiso público (anyone:reader)")

        url_view = f"https://drive.google.com/file/d/{file_id}/view" if file_id else None
        url_download = f"https://drive.google.com/uc?id={file_id}&export=download" if file_id else None

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

def get_sheets_service():
    json_creds = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if json_creds:
        try:
            creds_info = json.loads(json_creds)
            creds = Credentials.from_service_account_info(
                creds_info,
                scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
            )
            return build("sheets", "v4", credentials=creds)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al leer credenciales desde entorno: {e}")

    creds_path_env = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    if creds_path_env and Path(creds_path_env).exists():
        creds_path = Path(creds_path_env)
    else:
        creds_path = Path(__file__).resolve().parents[1] / "credentials.json"
        if not creds_path.exists():
            raise HTTPException(status_code=500, detail="No se encontró credentials.json ni GOOGLE_SERVICE_ACCOUNT_FILE")

    creds = Credentials.from_service_account_file(
        str(creds_path),
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return build("sheets", "v4", credentials=creds)

def read_sheet_data(spreadsheet_id: str, range_: str):
    sheets_service = get_sheets_service()
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    return result.get("values", [])
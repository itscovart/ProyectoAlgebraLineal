# services/drive_oauth.py
import os
import io
import json
import logging
from pathlib import Path
from fastapi import HTTPException

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def _load_credentials() -> Credentials:
    """
    Carga credenciales OAuth de usuario de una de estas fuentes:
    1) Variable de entorno GOOGLE_OAUTH_TOKEN_JSON (contenido del token.json)
    2) Archivo local token.json (para desarrollo)
    Si hay caducidad, las refresca usando client_id/secret (desde el token).
    """
    # 1) Railway / Producción: token en variable de entorno
    token_env = os.getenv("GOOGLE_OAUTH_TOKEN_JSON")
    if token_env:
        try:
            data = json.loads(token_env)
            creds = Credentials.from_authorized_user_info(data, SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Token OAuth inválido en entorno: {e}")

    # 2) Local: token.json en disco (generado con flujo de autorización)
    token_path = Path("token.json")
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds

    raise HTTPException(
        status_code=500,
        detail="No hay token OAuth (GOOGLE_OAUTH_TOKEN_JSON o token.json). "
               "Genera token localmente con el script de autorización."
    )

def get_drive_service():
    creds = _load_credentials()
    try:
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        logging.exception("No se pudo construir el servicio de Drive")
        raise HTTPException(status_code=500, detail=f"Error creando servicio Drive: {e}")

def upload_bytes_to_drive(contenido: bytes, filename: str, mime: str, folder_id: str, make_public: bool = True):
    """
    Sube 'contenido' como archivo a Mi unidad (del usuario autenticado por OAuth)
    en la carpeta 'folder_id'. Si make_public=True, agrega permiso 'anyone: reader'.
    Devuelve URLs de visualización/descarga.
    """
    try:
        service = get_drive_service()

        file_metadata = {"name": filename}
        if folder_id:
            file_metadata["parents"] = [folder_id]

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
        logging.exception("Error subiendo a Google Drive con OAuth de usuario")
        raise HTTPException(status_code=502, detail=f"Error subiendo a Google Drive (OAuth): {e}")
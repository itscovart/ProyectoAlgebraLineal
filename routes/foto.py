from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from pathlib import Path
import uuid, os

from services.drive_oauth import upload_bytes_to_drive
from database.insert_foto import insert_imagen_link

router = APIRouter()

DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

@router.post("/procesar")
async def procesar_foto(archivo: UploadFile = File(...), matriz: str = Form(...)):
    if not archivo.content_type or not archivo.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Solo se aceptan archivos de imagen (JPEG, PNG, WEBP, etc.).")

    suffix = Path(archivo.filename).suffix if archivo.filename else ""
    fname = f"img_{uuid.uuid4().hex}{suffix}"

    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    drive_resp = upload_bytes_to_drive(
        contenido=contenido,
        filename=fname,
        mime=archivo.content_type or "application/octet-stream",
        folder_id=DRIVE_FOLDER_ID,
        make_public=True,
    )

    url_para_guardar = drive_resp["url_view"]

    insert_imagen_link(url_para_guardar, matriz)

    return {
        "ok": True,
        "url": url_para_guardar,
        "drive_file_id": drive_resp["id"],
    }
"""
Ruta FastAPI para recibir una imagen, subirla a Google Drive y registrar su URL en la base de datos.
"""

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from pathlib import Path
import uuid, os

from services.drive_oauth import upload_bytes_to_drive
from database.insert_foto import insert_imagen_link

# Inicializamos el router para agrupar las rutas relacionadas con imagenes.
router = APIRouter()

# Carpeta de Google Drive donde se guardarán las imagenes.
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

"""
Endpoint para procesar una imagen subida por el usuario.
Valida el archivo, lo sube a Drive y guarda su URL asociada a una matriz.
"""
@router.post("/procesar")
async def procesar_foto(archivo: UploadFile = File(...), matriz: str = Form(...)):
    # Validamos que el archivo realmente sea una imagen.
    if not archivo.content_type or not archivo.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Solo se aceptan archivos de imagen (JPEG, PNG, WEBP, etc.).")

    # Creamos un nombre unico para evitar colisiones en Drive.
    suffix = Path(archivo.filename).suffix if archivo.filename else ""
    fname = f"img_{uuid.uuid4().hex}{suffix}"

    # Leemos el contenido binario del archivo subido.
    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    # Subimos la imagen a Google Drive mediante la función auxiliar.
    drive_resp = upload_bytes_to_drive(
        contenido=contenido,
        filename=fname,
        mime=archivo.content_type or "application/octet-stream",
        folder_id=DRIVE_FOLDER_ID,
        make_public=True,
    )

    url_para_guardar = drive_resp["url_view"]

    # Guardamos la URL de la imagen en la base de datos vinculada a la matriz.
    insert_imagen_link(url_para_guardar, matriz)

    return {
        "ok": True,
        "url": url_para_guardar,
        "drive_file_id": drive_resp["id"],
    }
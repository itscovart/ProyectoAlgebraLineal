from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from services import determinante, inversa, sel
from utils import archivo_matriz
import copy
import logging 
from services.registro_db import registrar_resultado_prueba 

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/procesar')
async def procesar_matriz(
    operacion: str = Form(...),
    archivo: UploadFile = File(...),
):
    texto = await archivo.read()
    contenido = texto.decode('utf-8')
    matriz = archivo_matriz.convertir_txt_matriz(contenido=contenido, separador=",")
    
    if(operacion == "Determinante"):
        respuesta = determinante.obtener_determinante(copy.deepcopy(matriz))
    elif(operacion == "SEL"):
        respuesta = sel.resolver_matriz(copy.deepcopy(matriz))
    elif(operacion == "Inversa"):
        respuesta = inversa.obtener_inversa(copy.deepcopy(matriz))
    else:
        raise HTTPException(status_code=400, detail="Operacion no valida")
    
    comentario, matrices_solucion, id_pasos = respuesta
    
    datos_respuesta = {
        "operacion": operacion,
        "matriz_inicial": matriz,
        "comentario": comentario,
        "matrices_pasos": matrices_solucion,
        "matrices_pasos_id": id_pasos
    }
    validacionesAD = [1, 0, 1, 1, 0, 1]
    validacionesM = [1, 0, 1, 1, 1, 1, 1, 1]
    validacionesD = [1, 1]
    validacionesBP = [1, 1, 1, 1, 1]
    registrosDrive = [1, 1, "Link1", "Link2"]
    try:
        exito_registro = registrar_resultado_prueba(datos_respuesta, validacionesAD, validacionesM, validacionesD, validacionesBP, registrosDrive)
        if not exito_registro:
            logger.warning("Fallo al registrar la prueba en la base de datos.")
    except Exception as e:
        logger.error(f"Excepción al intentar registrar en DB: {e}")

    return datos_respuesta
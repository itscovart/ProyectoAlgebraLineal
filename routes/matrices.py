"""
Rutas para procesar archivos de matrices y ejecutar operaciones como
determinante, inversa o resolución de sistemas lineales.
"""

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from services import determinante, inversa, sel
from utils import archivo_matriz, registrar_validaciones
import copy
import logging 
from services.registro_db import registrar_resultado_prueba 

# Router principal para las operaciones con matrices.
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/procesar')
async def procesar_matriz(
    operacion: str = Form(...),
    archivo: UploadFile = File(...),
):
    """
    Endpoint que recibe un archivo de texto con una matriz y ejecuta
    la operación solicitada (Determinante, SEL, Inversa).
    """
    # Leemos el archivo subido por el usuario.
    texto = await archivo.read()
    contenido = texto.decode('utf-8')
    # Convertimos el contenido del archivo a una matriz numérica.
    matriz = archivo_matriz.convertir_txt_matriz(contenido=contenido, separador=",")
    
    # Ejecutamos la operación correspondiente usando los servicios del sistema.
    if(operacion == "Determinante"):
        respuesta = determinante.obtener_determinante(copy.deepcopy(matriz))
    elif(operacion == "SEL"):
        respuesta = sel.resolver_matriz(copy.deepcopy(matriz))
    elif(operacion == "Inversa"):
        respuesta = inversa.obtener_inversa(copy.deepcopy(matriz))
    else:
        raise HTTPException(status_code=400, detail="Operacion no valida")
    
    comentario, matrices_pasos, id_pasos = respuesta    
    
    # Construimos la respuesta que se devolverá al cliente.
    datos_respuesta = {
        "operacion": operacion,
        "matriz_inicial": matriz,
        "comentario": comentario,
        "matrices_pasos": matrices_pasos,
        "matrices_pasos_id": id_pasos
    }
    # Ejecutamos validaciones auxiliares (anti-dumbs, matematicas, diseño, etc.).
    validacionesAD = registrar_validaciones.validarAD()
    if(operacion != "SEL"):
        validacionesM = registrar_validaciones.validarM(matriz_cuadrada=1, matriz_aumentada=0)
    else:
        validacionesM = registrar_validaciones.validarM(matriz_cuadrada=0, matriz_aumentada=1)
    validacionesD = registrar_validaciones.validarD()
    validacionesBP = registrar_validaciones.validarBP()
    registrosDrive = registrar_validaciones.validarDrive(matriz=matriz, comentario=comentario, respuesta_inversa=matrices_pasos)
    # Intentamos registrar los resultados de la prueba en la base de datos.
    try:
        exito_registro = registrar_resultado_prueba(datos_respuesta, validacionesAD, validacionesM, validacionesD, validacionesBP, registrosDrive)
        if not exito_registro:
            logger.warning("Fallo al registrar la prueba en la base de datos.")
    except Exception as e:
        logger.error(f"Excepción al intentar registrar en DB: {e}")

    # Devolvemos al cliente toda la informacion procesada.
    return datos_respuesta
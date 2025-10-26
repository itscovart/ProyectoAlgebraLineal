from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from services import determinante, inversa, sel
from utils import procesar_respuesta, archivo_matriz
import numpy as np

router = APIRouter()

@router.post('/procesar')
async def procesar_matriz(
  operacion: str = Form(...),
  archivo: UploadFile = File(...),
):
  texto = await archivo.read()
  contenido = texto.decode('utf-8')
  matriz = archivo_matriz.convertir_txt_matriz(contenido=contenido, separador=",")
  matriz_np = np.array(matriz)
  
  if(operacion == "Determinante"):
    respuesta = determinante.obtener_determinante(matriz_np)
  elif(operacion == "SEL"):
    respuesta = sel.resolver_matriz(matriz_np)
  elif(operacion == "Inversa"):
    respuesta = inversa.obtener_inversa(matriz_np)
  else:
    raise HTTPException(status_code=400, detail="Operacion no valida")
  
  comentario, matrices_solucion, id_pasos = procesar_respuesta.procesar_respuestas_operacion()
  
  return {
    "operacion": operacion,
    "matriz_inicial": matriz,
    "comentario": comentario,
    "matrices_pasos": matrices_solucion,
    "matrices_pasos_id": id_pasos
  }
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from services import determinante, inversa, sel
from utils import archivo_matriz

router = APIRouter()

@router.post('/procesar')
async def procesar_matriz(
  operacion: str = Form(...),
  archivo: UploadFile = File(...),
):
  texto = await archivo.read()
  contenido = texto.decode('utf-8')
  matriz = archivo_matriz.convertir_txt_matriz(contenido=contenido, separador=",")
  
  if(operacion == "Determinante"):
    respuesta = determinante.obtener_determinante(matriz)
  elif(operacion == "SEL"):
    respuesta = sel.resolver_matriz(matriz)
  elif(operacion == "Inversa"):
    respuesta = inversa.obtener_inversa(matriz)
  else:
    raise HTTPException(status_code=400, detail="Operacion no valida")
  
  comentario, matrices_solucion, id_pasos = respuesta
  
  return {
    "operacion": operacion,
    "matriz_inicial": matriz,
    "comentario": comentario,
    "matrices_pasos": matrices_solucion,
    "matrices_pasos_id": id_pasos
  }
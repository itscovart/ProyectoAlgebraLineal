from fastapi import HTTPException
from services import validaciones

def convertir_txt_matriz(contenido: str, separador: str = ",") -> list[list[float]]:
  filas = contenido.splitlines()
  try:
    matriz = [[float(x) for x in fila.split(separador)] for fila in filas]
  except:
    raise HTTPException(status_code=400, detail="Error!, Recuerda que solo se aceptan matrices con numeros") 
  if not (validaciones.validar_tamaño_filas(matriz=matriz)):
    error = "Error! Recuerda que solo se pueden hacer operaciones de matrices cuando todas las filas tienen la misma cantidad de elementos"
    raise HTTPException(status_code=400, detail=error)
  return matriz
from fastapi import HTTPException
import numpy as np
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
  # filas = contenido.splitlines()
  # matriz = []

  # for fila in filas:
  #     try:
  #         valores = [float(x.strip()) for x in fila.split(separador) if x.strip() != ""]
  #         matriz.append(valores)
  #     except ValueError:
  #         # Aquí atrapas el error de conversión
  #         raise HTTPException(
  #             status_code=400,
  #             detail="Error! Recuerda que solo se pueden hacer operaciones con números."
  #         )

  # validar_matriz = validaciones.validaciones_generales(matriz=matriz)
  # if False in validar_matriz:
  #     match validar_matriz.index(False):
  #         case 0:
  #             error = "Error! Recuerda que todas las filas deben tener la misma cantidad de columnas."
  #         case 1:
  #             error = "Error! Recuerda que solo se pueden hacer operaciones con números."
  #     raise HTTPException(status_code=400, detail=error)

  # return matriz
from fastapi import HTTPException
from services import validaciones

def convertir_txt_matriz(contenido: str, separador: str = ",") -> list[list[float]]:
  filas = contenido.splitlines()
  try:
    matriz = []
    for fila in filas:
      fila_valores = []
      for x in fila.split(separador):
        if '/' in x:
          a, b = x.split('/')
          valor = float(a) / float(b)
        else:
          valor = float(x)
        fila_valores.append(valor)
      matriz.append(fila_valores)
  except:
    raise HTTPException(status_code=400, detail="Error!, Recuerda que solo se aceptan matrices con numeros y con el formato correcto")
  if not (validaciones.validar_tamaño_filas(matriz=matriz)):
    error = "Error! Recuerda que solo se pueden hacer operaciones de matrices cuando todas las filas tienen la misma cantidad de elementos"
    raise HTTPException(status_code=400, detail=error)
  return matriz
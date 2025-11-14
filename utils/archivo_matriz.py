"""
Funciones para convertir contenido de texto en una matriz numérica.
Permite interpretar números normales y fracciones, y valida el tamaño de las filas.
"""
from fastapi import HTTPException
from services import validaciones
from utils.convertidores import obtener_valor_fraccion

"""
Convierte un texto recibido (generalmente desde un archivo .txt)
en una matriz numérica (lista de listas).

Parámetros:
  contenido : str  -> texto completo del archivo
  separador : str  -> carácter que separa los valores (por defecto coma)

Retorna:
  matriz (list[list[float]]) -> matriz numérica validada

Lanza:
  HTTPException si el formato es incorrecto o si las filas no son uniformes.
"""

def convertir_txt_matriz(contenido: str, separador: str = ",") -> list[list[float]]:
  # Dividimos el contenido en filas según saltos de línea.
  filas = contenido.splitlines()
  try:
    # Aquí almacenaremos cada fila convertida a valores numéricos.
    matriz = []
    # Recorremos cada fila del texto original.
    for fila in filas:
      # Lista temporal para guardar los valores de la fila actual.
      fila_valores = []
      # Separamos la fila en sus elementos usando el separador indicado.
      for x in fila.split(separador):
        # Si el elemento contiene '/', lo interpretamos como fracción.
        if '/' in x:
          valor = obtener_valor_fraccion(x)
        # En caso contrario, convertimos el número directamente a float.
        else:
          valor = float(x)
        fila_valores.append(valor)
      # Agregamos la fila convertida a la matriz final.
      matriz.append(fila_valores)
  # Si ocurre un error en la conversión, significa que el formato es inválido.
  except:
    raise HTTPException(status_code=400, detail="Error!, Recuerda que solo se aceptan matrices con numeros y con el formato correcto")
  # Validamos que todas las filas tengan la misma cantidad de columnas.
  if not (validaciones.validar_tamaño_filas(matriz=matriz)):
    error = "Error! Recuerda que solo se pueden hacer operaciones de matrices cuando todas las filas tienen la misma cantidad de elementos"
    raise HTTPException(status_code=400, detail=error)
  # Devolvemos la matriz ya convertida y validada.
  return matriz
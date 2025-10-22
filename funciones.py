"""
  Funcion para intercambiar filas
  Input: matriz, fila a cambiar, fila destino
  Output: Matriz con filas intercambiadas
"""

def Intercambiar_filas(matriz, fila_base, fila_destino) -> list:
  temp = matriz[fila_base]
  matriz[fila_base] = matriz[fila_destino]
  matriz[fila_destino] = temp
  return matriz

"""
  Funcion para hacer uno el pivote y todos los elementos de su fila
  Input: fila completa e indice de las columnas del pivote
  Output: Matriz con fila afectada y pivote igual a 1
"""
def Hacer_uno_pivote(fila, indice_columna) -> list:
  pivote = 1/fila[indice_columna]
  for i, valor in enumerate(fila):
    fila[i] = pivote * valor
  return fila

"""
  Funcion para hacer ceros abajo del pivote
  Input: matriz e indice del pivote
  Output: Matriz con filas afectadas
"""
def Hacer_cero_abajo(matriz, indice_pivote) -> list:
  if(indice_pivote == (len(matriz) - 1)):
    res = matriz
  else:
    for i, fila in enumerate(matriz[indice_pivote + 1:], indice_pivote + 1):
      factor = matriz[i][indice_pivote]
      for j, _ in enumerate(fila):
        matriz[i][j] -= factor * matriz[indice_pivote][j]
    res = matriz
  return res

"""
  Funcion para hacer ceros arriba del pivote
  Input: matriz e indice del pivote
  Output: Matriz con filas afectadas
"""
def Hacer_cero_arriba(matriz, indice_pivote) -> list:
  if(indice_pivote == 0):
    res = matriz
  else:
    for i, fila in enumerate(matriz[:indice_pivote]):
      factor = matriz[i][indice_pivote]
      for j, _ in enumerate(fila):
        matriz[i][j] -= factor * matriz[indice_pivote][j]
    res = matriz
  return res

"""
  Funcion para imprimir con formato adecuado la matriz resultante
  Input: matriz
"""
def ImprimirMatriz(matriz):
  for fila in matriz:
    print(f"{fila}\n")

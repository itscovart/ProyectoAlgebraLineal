import copy

"""
  Funcion para intercambiar filas
  Input: matriz, fila a cambiar, fila destino
  Output: Matriz con filas intercambiadas
"""

def Intercambiar_filas(matriz, fila_base, fila_destino) -> list:
  nueva_matriz = copy.deepcopy(matriz)
  temp = nueva_matriz[fila_base]
  nueva_matriz[fila_base] = nueva_matriz[fila_destino]
  nueva_matriz[fila_destino] = temp
  return nueva_matriz

"""
  Funcion para hacer uno el pivote y todos los elementos de su fila
  Input: fila completa e indice de las columnas del pivote
  Output: Matriz con fila afectada y pivote igual a 1
"""
def Hacer_uno_pivote(fila, indice_columna) -> list:
  nueva_fila = fila.copy()
  pivote = 1/nueva_fila[indice_columna]
  factor = nueva_fila[indice_columna]
  for i, valor in enumerate(nueva_fila):
    nueva_fila[i] = pivote * valor
  return nueva_fila, factor

"""
  Funcion para hacer ceros abajo del pivote
  Input: matriz e indice del pivote
  Output: Matriz con filas afectadas
"""
def Hacer_cero_abajo(matriz, indice_pivote) -> list:
  nueva_matriz = copy.deepcopy(matriz)
  if(indice_pivote == (len(nueva_matriz) - 1)):
    res = nueva_matriz
  else:
    for i, fila in enumerate(nueva_matriz[indice_pivote + 1:], indice_pivote + 1):
      factor = nueva_matriz[i][indice_pivote]
      for j, _ in enumerate(fila):
        nueva_matriz[i][j] -= factor * nueva_matriz[indice_pivote][j]
    res = nueva_matriz
  return res

"""
  Funcion para hacer ceros arriba del pivote
  Input: matriz e indice del pivote
  Output: Matriz con filas afectadas
"""
def Hacer_cero_arriba(matriz, indice_pivote) -> list:
  nueva_matriz = copy.deepcopy(matriz)
  if(indice_pivote == 0):
    res = nueva_matriz
  else:
    for i, fila in enumerate(nueva_matriz[:indice_pivote]):
      factor = nueva_matriz[i][indice_pivote]
      for j, _ in enumerate(fila):
        nueva_matriz[i][j] -= factor * nueva_matriz[indice_pivote][j]
    res = nueva_matriz
  return res

def encontrar_pivote_nuevo(matriz, indice_inicial) -> int:
  indice = indice_inicial
  for i in range(indice_inicial + 1, len(matriz)):
    if matriz[i][indice_inicial] != 0:
      indice = i
      break
  return indice
  
def concatenar_matrices(matriz_izquierda, matriz_derecha):
    matriz_izquierda = copy.deepcopy(matriz_izquierda)
    matriz_derecha = copy.deepcopy(matriz_derecha)
    matriz_unida = [fila_izq + fila_der for fila_izq, fila_der in zip(matriz_izquierda, matriz_derecha)]
    return matriz_unida
  
"""
  Funcion para imprimir con formato adecuado la matriz resultante
  Input: matriz
"""
def ImprimirMatriz(matriz):
  for fila in matriz:
    print(f"{fila}\n")
    
"""
  Funcion para generar una matriz identidad con definicion
  aij <- 1 si i == j sino 0
  Output: Matriz cuadrada identidad
"""
def crear_matriz_identidad(tamaño):
  matriz_identidad = [[1 if i == j else 0 for j in range(tamaño)] for i in range(tamaño)]
  return matriz_identidad
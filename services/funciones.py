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

def Hacer_cero_abajo_ij(matriz, fila_pivote, col_pivote) -> list:
  """
  Hace ceros por debajo en la columna col_pivote usando la fila fila_pivote como pivote.
  No asume pivote en a_ii.
  """
  nueva_matriz = copy.deepcopy(matriz)
  m = len(nueva_matriz)
  if fila_pivote >= m - 1:
    return nueva_matriz
  for i in range(fila_pivote + 1, m):
    factor = nueva_matriz[i][col_pivote]
    if factor != 0:
      for j in range(len(nueva_matriz[i])):
        nueva_matriz[i][j] -= factor * nueva_matriz[fila_pivote][j]
  return nueva_matriz

def Hacer_cero_arriba_ij(matriz, fila_pivote, col_pivote) -> list:
  """
  Hace ceros por arriba en la columna col_pivote usando la fila fila_pivote como pivote.
  No asume pivote en a_ii.
  """
  nueva_matriz = copy.deepcopy(matriz)
  if fila_pivote <= 0:
    return nueva_matriz
  for i in range(0, fila_pivote):
    factor = nueva_matriz[i][col_pivote]
    if factor != 0:
      for j in range(len(nueva_matriz[i])):
        nueva_matriz[i][j] -= factor * nueva_matriz[fila_pivote][j]
  return nueva_matriz

def buscar_siguiente_pivote(matriz, fila_inicio, col_inicio, n_cols_izq):
  """
  Recorre columnas desde col_inicio y busca una fila >= fila_inicio con entrada != 0.
  Devuelve (fila_pivote, col_pivote) o (None, None) si ya no hay pivotes.
  """
  if not matriz or not matriz[0]:
    return None, None
  num_cols = min(n_cols_izq, len(matriz[0]))
  num_filas = len(matriz)
  for j in range(col_inicio, num_cols):
    for i in range(fila_inicio, num_filas):
      if matriz[i][j] != 0:
        return i, j
  return None, None

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

def separar_matriz_aumentada(matriz):
  coeficientes = copy.deepcopy([fila[:-1] for fila in matriz])
  igualdades = copy.deepcopy([[fila[-1]] for fila in matriz])
  return coeficientes, igualdades

def procesar_solucion_sel_por_pivotes(matriz, pivot_cols):
  """
  'pivot_cols' es la lista (por fila de pivote) de índices de columnas del bloque izquierdo donde cayó cada pivote.
  Reporta variables pivote con su valor y marca libres las demás, sin reordenar columnas.
  """
  inconsistencia, fila_inconsistencia = validar_incosistencia_sel(matriz=matriz)
  if inconsistencia:
    return f"El sistema de ecuaciones lineales no tiene conjunto solucion debido a una inconsistencia en la ecuacion resultante {fila_inconsistencia + 1}"
  
  coeficientes, igualdades = separar_matriz_aumentada(matriz=matriz)
  n = len(coeficientes[0]) if coeficientes else 0
  pivot_set = set(pivot_cols)
  solucion = {}
  # Variables pivote: valor tomado del RHS de su fila
  for fila_idx, col_idx in enumerate(pivot_cols):
    if col_idx is not None and col_idx < n:
      solucion[f"v{col_idx + 1}"] = igualdades[fila_idx][0]
  # Variables libres: columnas que no aparecen en pivot_set
  for col in range(n):
    if col not in pivot_set:
      solucion[f"v{col + 1}"] = " ∈ ℝ"
  return solucion

def obtener_dict_valores_sel(claves, valores):
  solucion = {}
  for k, v in zip(claves, valores):
      solucion[k] = v
  return solucion

def validar_incosistencia_sel(matriz):
  resultado = [False, 0]
  for i, fila in enumerate(matriz):
    if all(valor == 0 for valor in fila[:-1]) and fila[-1] != 0:
      resultado = [True, i]
      break
  return resultado
    
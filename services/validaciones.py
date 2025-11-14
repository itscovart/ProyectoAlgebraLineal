"""
Funciones de validación utilizadas en operaciones de Álgebra Lineal.
Verifican tamaños de matrices, cuadratura, existencia de filas/columnas de ceros
y requisitos mínimos para resolver SEL.
"""

"""
Valida que todas las filas de una matriz tengan el mismo tamaño.
Output: True si todas las filas son uniformes, False si alguna difiere.
"""
def validar_tamaño_filas(matriz) -> bool:
  # El tamaño esperado de cada fila es el de la primera fila.
  tamaño = len(matriz[0])
  # Recorremos cada fila y verificamos que tenga el mismo número de columnas.
  respuesta = True
  for fila in matriz:
    if(len(fila) != tamaño):
      respuesta = False
      break
  return respuesta

"""
Verifica si una matriz es cuadrada (mismo número de filas y columnas).
"""
def validar_matriz_cuadrada(matriz) -> bool:
  columnas, filas = len(matriz[0]), len(matriz)
  return columnas == filas

"""
Determina si existe al menos una fila compuesta únicamente por ceros.
"""
def validar_existencia_filas_ceros(matriz) -> bool:
  existencia_puros_ceros = False
  for fila in matriz:
    # all(...) devuelve True solo si todos los valores de la fila son 0.
    if all(valor == 0 for valor in fila):
      existencia_puros_ceros = True
  return existencia_puros_ceros

"""
Verifica si existe alguna columna formada completamente por ceros.
"""
def validar_existencia_columnas_ceros(matriz) -> bool:
  tamaño = len(matriz)
  existencia_puros_ceros = False
  # Recorremos cada columna verificando si todos sus elementos son 0.
  for j in range(tamaño):
    if all(matriz[i][j] == 0 for i in range(tamaño)):
      existencia_puros_ceros = True
  return existencia_puros_ceros

"""
Valida que una matriz aumentada [A|b] tenga el tamaño mínimo para un SEL:
al menos 1 fila y al menos 2 columnas.
"""
def validar_tamaño_minimo_sel(matriz):
  filas = len(matriz)
  columnas = len(matriz[0])
  # Debe haber mínimo una ecuación (fila) y al menos una variable + b (2 columnas).
  return filas >= 1 and columnas >= 2
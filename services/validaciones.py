def validar_tamaño_filas(matriz) -> bool:
  respuesta = True
  tamaño = len(matriz[0])
  for fila in matriz:
    if(len(fila) != tamaño):
      respuesta = False
      break
  return respuesta

def validar_matriz_cuadrada(matriz) -> bool:
  columnas, filas = len(matriz[0]), len(matriz)
  return columnas == filas

def validar_existencia_filas_ceros(matriz) -> bool:
  existencia_puros_ceros = False
  for fila in matriz:
    if all(valor == 0 for valor in fila):
      existencia_puros_ceros = True
  return existencia_puros_ceros

def validar_existencia_columnas_ceros(matriz) -> bool:
  tamaño = len(matriz)
  existencia_puros_ceros = False
  for j in range(tamaño):
    if all(matriz[i][j] == 0 for i in range(tamaño)):
      existencia_puros_ceros = True
  return existencia_puros_ceros

def validar_tamaño_minimo_sel(matriz):
  filas = len(matriz)
  columnas = len(matriz[0])
  return filas >= 1 and columnas >= 2
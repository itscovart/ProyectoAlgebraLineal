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
  for fila in matriz:
    existencia_ceros = False
    for valor in fila:
      if(valor == 0):
        existencia_ceros = True
        break
    if(existencia_ceros == True):
      break
  return existencia_ceros

def validar_existencia_columnas_ceros(matriz) -> bool:
  tamaño = len(matriz)
  for j in range(tamaño):
    existencia_ceros = False
    for i in range(tamaño):
      if(matriz[i][j] == 0):
        existencia_ceros = True
        break
    if(existencia_ceros == True):
      break
  return existencia_ceros
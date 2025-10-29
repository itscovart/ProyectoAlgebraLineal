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

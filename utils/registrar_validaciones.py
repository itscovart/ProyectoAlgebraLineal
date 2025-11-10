def validarAD() -> list:
  return [1, 0, 1, 1, 0, 1]

def validarM(matriz_cuadrada, matriz_aumentada, valido) -> list:
  return [matriz_cuadrada, matriz_aumentada, 1, 1, 1, 1, 1, 1] if valido else [0, 0, 0, 0, 0, 0, 0, 0]

def validarD():
  return [1, 1]

def validarBP():
  return [1, 1, 1, 1, 1] 

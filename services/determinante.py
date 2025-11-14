import copy
from services import funciones, validaciones

def Gauss_Jordan_Determinante(matriz):
  pasos = []
  id_pasos = []
  solucion = True
  matriz = copy.deepcopy(matriz)
  
  if not (validaciones.validar_existencia_filas_ceros(matriz=matriz) or validaciones.validar_existencia_columnas_ceros(matriz=matriz)):
    valor_determinante = 1
    tamaño = len(matriz[0])

    i = 0 
    j = 0

    while i < tamaño and j < tamaño:
      fila_piv, col_piv = funciones.buscar_siguiente_pivote(matriz=matriz, fila_inicio=i, col_inicio=j, n_cols_izq=tamaño)
      if fila_piv is None:
        solucion = False
        valor_determinante = 0
        break

      if fila_piv != i:
        matriz = funciones.Intercambiar_filas(matriz=matriz, fila_base=i, fila_destino=fila_piv)
        pasos.append(copy.deepcopy(matriz))
        id_pasos.append([1, i, fila_piv]) 
        valor_determinante *= -1

      pivote = matriz[i][col_piv]
      if pivote == 0:
        solucion = False
        valor_determinante = 0
        break

      if pivote != 1:
        matriz[i], factor = funciones.Hacer_uno_pivote(fila=matriz[i], indice_columna=col_piv)
        pasos.append(copy.deepcopy(matriz))
        id_pasos.append([2, factor])
        valor_determinante *= factor

      if i != (len(matriz) - 1):
        matriz = funciones.Hacer_cero_abajo_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
        pasos.append(copy.deepcopy(matriz)); id_pasos.append([3, i, col_piv])
      if i != 0:
        matriz = funciones.Hacer_cero_arriba_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
        pasos.append(copy.deepcopy(matriz)); id_pasos.append([4, i, col_piv])

      i += 1
      j = col_piv + 1
      
    if i < tamaño:
      solucion = False
      valor_determinante = 0
  
  else:
    valor_determinante = 0
    solucion = False
  
  return valor_determinante, pasos, id_pasos, solucion
def obtener_determinante(matriz) -> list:
  if(validaciones.validar_matriz_cuadrada(matriz=matriz) == True):
    valor_determinante, matriz_pasos, id_pasos, solucion = Gauss_Jordan_Determinante(matriz=matriz)
    respuesta = [f"La matriz tiene como determinante {valor_determinante}", matriz_pasos, id_pasos] if solucion == True else ["La matriz tiene como determinante 0 debido a la existencia de un 0 en la diagonal principal", matriz_pasos, id_pasos]
  else:
    respuesta = ["La determinante solo se puede obtener de matrices cuadradas", 0, 0]
  return respuesta
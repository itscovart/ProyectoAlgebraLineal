import copy
from services import funciones, validaciones

def Gauss_Jordan_Determinante(matriz):
  pasos = []
  id_pasos = []
  solucion = True
  
  if not (validaciones.validar_existencia_filas_ceros(matriz=matriz) or validaciones.validar_existencia_columnas_ceros(matriz=matriz)):
    valor_determinante = 1
    for i, fila in enumerate(matriz):
      pivote = matriz[i][i]
      if(pivote == 0):
        nuevo_indice = funciones.encontrar_pivote_nuevo(matriz=matriz, indice_inicial=i)
        if(nuevo_indice == i):
          solucion = False
          valor_determinante = 0
          break
        else:
          matriz = funciones.Intercambiar_filas(matriz=matriz, fila_base=i, fila_destino=nuevo_indice)
          pasos.append(copy.deepcopy(matriz))
          id_pasos.append([1, i, nuevo_indice])
          valor_determinante *= -1
          pivote = matriz[i][i]
      if(pivote != 1):
        matriz[i], factor = funciones.Hacer_uno_pivote(fila=matriz[i], indice_columna=i)
        pasos.append(copy.deepcopy(matriz))
        id_pasos.append([2, factor])
        valor_determinante *= factor
      matriz = funciones.Hacer_cero_abajo(matriz=matriz, indice_pivote=i)
      pasos.append(copy.deepcopy(matriz))
      id_pasos.append([3])
      matriz = funciones.Hacer_cero_arriba(matriz=matriz, indice_pivote=i)
      pasos.append(copy.deepcopy(matriz))
      id_pasos.append([4])
  else:
    valor_determinante = 0
  return valor_determinante, pasos, id_pasos, solucion
def obtener_determinante(matriz) -> list:
  if(validaciones.validar_matriz_cuadrada(matriz=matriz) == True):
    valor_determinante, matriz_pasos, id_pasos, solucion = Gauss_Jordan_Determinante(matriz=matriz)
    respuesta = [f"La matriz tiene como determinante {valor_determinante}", matriz_pasos, id_pasos] if solucion == True else ["La matriz tiene como determinante 0 debido a la existencia de un 0 en la diagonal principal", matriz_pasos, id_pasos]
  else:
    respuesta = ["La determinante solo se puede obtener de matrices cuadradas", 0, 0]
  return respuesta
  
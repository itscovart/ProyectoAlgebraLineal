"""
Funciones para calcular la determinante de una matriz usando
el método de Gauss‑Jordan y registrar los pasos realizados.
"""
import copy
from services import funciones, validaciones

"""
Función para obtener la determinante aplicando Gauss‑Jordan.
Input: matriz cuadrada.
Output: (valor_determinante, pasos, id_pasos, solucion_bool).
"""
def Gauss_Jordan_Determinante(matriz):
  # Lista donde se almacena cada estado intermedio de la matriz.
  pasos = []
  # Lista que guarda el tipo de operación realizada en cada paso.
  id_pasos = []
  # Definimos solucion como verdadera por defecto
  solucion = True
  # Copiamos la matriz original para no modificarla directamente.
  matriz = copy.deepcopy(matriz)
  
  # Verificamos si existe una fila o columna completa de ceros; de ser así, la determinante es 0.
  if not (validaciones.validar_existencia_filas_ceros(matriz=matriz) or validaciones.validar_existencia_columnas_ceros(matriz=matriz)):
    # La determinante empieza en 1 y se ajusta conforme avanzan las operaciones.
    valor_determinante = 1
    tamaño = len(matriz[0])

    i = 0 
    j = 0

    # Recorremos fila por fila buscando el siguiente pivote.
    while i < tamaño and j < tamaño:
      # Ubicamos el siguiente pivote válido dentro de la matriz.
      fila_piv, col_piv = funciones.buscar_siguiente_pivote(matriz=matriz, fila_inicio=i, col_inicio=j, n_cols_izq=tamaño)
      # Si no se encontró pivote, el determinante es 0 debido a que ya no hay otro posible pivote != 0.
      if fila_piv is None:
        solucion = False
        valor_determinante = 0
        break

      # Si el pivote no está en la fila actual, intercambiamos filas.
      if fila_piv != i:
        matriz = funciones.Intercambiar_filas(matriz=matriz, fila_base=i, fila_destino=fila_piv)
        pasos.append(copy.deepcopy(matriz))
        id_pasos.append([1, i, fila_piv]) 
        # Al intercambiar filas, el signo de la determinante se invierte.
        valor_determinante *= -1

      # Obtenemos el valor actual del pivote.
      pivote = matriz[i][col_piv]
      # Un pivote cero implica matriz no invertible → determinante 0.
      if pivote == 0:
        solucion = False
        valor_determinante = 0
        break

      # Iteramos la fila para convertir el pivote en 1.
      if pivote != 1:
        matriz[i], factor = funciones.Hacer_uno_pivote(fila=matriz[i], indice_columna=col_piv)
        pasos.append(copy.deepcopy(matriz))
        id_pasos.append([2, factor])
        # Ajustamos la determinante por el factor aplicado a la fila.
        valor_determinante *= factor

      # Convertimos en 0 los valores debajo del pivote.
      if i != (len(matriz) - 1):
        matriz = funciones.Hacer_cero_abajo_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
        pasos.append(copy.deepcopy(matriz)); id_pasos.append([3, i, col_piv])
      # Convertimos en 0 los valores encima del pivote.
      if i != 0:
        matriz = funciones.Hacer_cero_arriba_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
        pasos.append(copy.deepcopy(matriz)); id_pasos.append([4, i, col_piv])

      i += 1
      j = col_piv + 1
      
    # Si no alcanzamos a procesar todas las filas, entonces su determinante es 0.
    if i < tamaño:
      solucion = False
      valor_determinante = 0
  
  # Caso alterno: una fila o columna completa de ceros implica determinante 0.
  else:
    valor_determinante = 0
    solucion = False
  
  return valor_determinante, pasos, id_pasos, solucion
"""
Función de alto nivel para obtener la determinante.
Primero valida que la matriz sea cuadrada.
"""
def obtener_determinante(matriz) -> list:
  # Validamos que la matriz sea cuadrada antes de proceder.
  if(validaciones.validar_matriz_cuadrada(matriz=matriz) == True):
    valor_determinante, matriz_pasos, id_pasos, solucion = Gauss_Jordan_Determinante(matriz=matriz)
    # Armamos la respuesta incluyendo el valor obtenido y los pasos realizados.
    respuesta = [f"La matriz tiene como determinante {valor_determinante}", matriz_pasos, id_pasos] if solucion == True else ["La matriz tiene como determinante 0 debido a la existencia de un 0 en la diagonal principal", matriz_pasos, id_pasos]
  # Si la matriz no es cuadrada, no existe determinante.
  else:
    respuesta = ["La determinante solo se puede obtener de matrices cuadradas", 0, 0]
  return respuesta
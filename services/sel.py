"""
Funciones para resolver Sistemas de Ecuaciones Lineales (SEL) usando
el método de Gauss‑Jordan. Se registran todos los pasos del proceso.
"""
import copy
from services import funciones, validaciones

"""
Aplica Gauss‑Jordan a un sistema dado por:
  coeficientes -> matriz A
  igualdades   -> vector columna b
Output:
  [solucion, pasos_sel, id_pasos]
donde se registran:
  - pasos_sel: estados intermedios de la matriz aumentada [A|b]
  - id_pasos : tipo de operación realizada en cada paso
"""
def gauss_jordan_sel(coeficientes, igualdades):
  # Lista donde almacenamos cada paso visual del proceso.
  pasos_sel = []
  # Identificadores de operaciones (swap, pivote, ceros, etc.).
  id_pasos = []
  # Unimos [A] y [b] para formar la matriz aumentada [A|b].
  matriz_unida = funciones.concatenar_matrices(matriz_izquierda=coeficientes, matriz_derecha=igualdades)
  # Número de ecuaciones (filas).
  m = len(coeficientes)
  # Número de variables (columnas de A).
  n = len(coeficientes[0])

  i = 0
  j = 0
  # Aquí guardamos las columnas donde cayó cada pivote.
  pivot_cols = []

  # Recorremos filas y columnas buscando pivotes válidos.
  while i < m and j < n:
    # Buscamos el siguiente pivote no nulo a partir de la posición actual (i, j).
    fila_piv, col_piv = funciones.buscar_siguiente_pivote(matriz=matriz_unida, fila_inicio=i, col_inicio=j, n_cols_izq=n)
    # Si no se encuentra pivote, ya no hay más operaciones posibles.
    if fila_piv is None:
      break

    # Si el pivote no está en la fila actual, intercambiamos filas.
    if fila_piv != i:
      matriz_unida = funciones.Intercambiar_filas(matriz=matriz_unida, fila_base=i, fila_destino=fila_piv)
      pasos_sel.append(copy.deepcopy(matriz_unida))
      id_pasos.append([1, i, fila_piv])

    # Iteramos la fila para que el pivote se vuelva 1.
    if matriz_unida[i][col_piv] != 1:
      matriz_unida[i], factor = funciones.Hacer_uno_pivote(fila=matriz_unida[i], indice_columna=col_piv)
      pasos_sel.append(copy.deepcopy(matriz_unida))
      id_pasos.append([2, factor])

    # Hacemos ceros debajo del pivote.
    if i != (len(matriz_unida) - 1):
      matriz_unida = funciones.Hacer_cero_abajo_ij(matriz=matriz_unida, fila_pivote=i, col_pivote=col_piv)
      pasos_sel.append(copy.deepcopy(matriz_unida)); id_pasos.append([3, i, col_piv])

    # Hacemos ceros arriba del pivote.
    if i != 0:
      matriz_unida = funciones.Hacer_cero_arriba_ij(matriz=matriz_unida, fila_pivote=i, col_pivote=col_piv)
      pasos_sel.append(copy.deepcopy(matriz_unida)); id_pasos.append([4, i, col_piv])

    # Guardamos la columna donde cayó el pivote para procesar la solución final.
    pivot_cols.append(col_piv)
    i += 1
    j = col_piv + 1

  # Interpretamos la solución: variables pivote y dependencias con las libres.
  solucion = funciones.procesar_solucion_sel_por_pivotes(matriz=matriz_unida, pivot_cols=pivot_cols)
  return [solucion, pasos_sel, id_pasos]

"""
Función de alto nivel que recibe una matriz aumentada [A|b],
valida su tamaño y resuelve el sistema con Gauss‑Jordan.
"""
def resolver_matriz(matriz):
  # Verificamos que la matriz tenga al menos 1x2 (mínimo para un SEL).
  if(validaciones.validar_tamaño_minimo_sel(matriz=matriz)):
    # Separamos la matriz aumentada en A (coeficientes) y b (igualdades).
    coeficientes, igualdades = funciones.separar_matriz_aumentada(matriz=matriz)
    resultado = gauss_jordan_sel(coeficientes=coeficientes, igualdades=igualdades)
  else:
    # Si no cumple con el tamaño mínimo, devolvemos un mensaje explicativo.
    resultado = ["La matriz no cumple con el tamaño minimo para poder resolver un sistema de ecuaciones que es de 1x2", 0, 0]
  return resultado
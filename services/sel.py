import copy
from services import funciones, validaciones

def gauss_jordan_sel(coeficientes, igualdades):
  pasos_sel = []
  id_pasos = []
  matriz_unida = funciones.concatenar_matrices(matriz_izquierda=coeficientes, matriz_derecha=igualdades)
  m = len(coeficientes)
  n = len(coeficientes[0])

  i = 0
  j = 0
  pivot_cols = []

  while i < m and j < n:
    fila_piv, col_piv = funciones.buscar_siguiente_pivote(matriz=matriz_unida, fila_inicio=i, col_inicio=j, n_cols_izq=n)
    if fila_piv is None:
      break

    if fila_piv != i:
      matriz_unida = funciones.Intercambiar_filas(matriz=matriz_unida, fila_base=i, fila_destino=fila_piv)
      pasos_sel.append(copy.deepcopy(matriz_unida))
      id_pasos.append([1, i, fila_piv])  # swap filas

    if matriz_unida[i][col_piv] != 1:
      matriz_unida[i], factor = funciones.Hacer_uno_pivote(fila=matriz_unida[i], indice_columna=col_piv)
      pasos_sel.append(copy.deepcopy(matriz_unida))
      id_pasos.append([2, factor])

    matriz_unida = funciones.Hacer_cero_abajo_ij(matriz=matriz_unida, fila_pivote=i, col_pivote=col_piv)
    pasos_sel.append(copy.deepcopy(matriz_unida)); id_pasos.append([3, col_piv])

    matriz_unida = funciones.Hacer_cero_arriba_ij(matriz=matriz_unida, fila_pivote=i, col_pivote=col_piv)
    pasos_sel.append(copy.deepcopy(matriz_unida)); id_pasos.append([4, col_piv])

    pivot_cols.append(col_piv)
    i += 1
    j = col_piv + 1

  solucion = funciones.procesar_solucion_sel_por_pivotes(matriz=matriz_unida, pivot_cols=pivot_cols)
  return solucion, pasos_sel, id_pasos
def resolver_matriz(matriz):
  if(validaciones.validar_tamaño_minimo_sel(matriz=matriz)):
    coeficientes, igualdades = funciones.separar_matriz_aumentada(matriz=matriz)
    solucion, matriz_pasos, id_matriz_pasos = gauss_jordan_sel(coeficientes=coeficientes, igualdades=igualdades)
    resultado = [solucion, matriz_pasos, id_matriz_pasos]
  else:
    resultado = ["La matriz no cumple con el tamaño minimo para poder resolver un sistema de ecuaciones que es de 1x2", 0, 0]
  return resultado
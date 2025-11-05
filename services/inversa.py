import copy
from services import funciones, validaciones, determinante

def Gauss_Jordan_Inversa(matriz, tamaño):
  pasos_inversa = []
  id_pasos_inversa = []
  solucion = True
  
  m = len(matriz)
  n_total = len(matriz[0])
  n_izq = tamaño

  i = 0
  j = 0

  while i < tamaño and j < n_izq:
    fila_piv, col_piv = funciones.buscar_siguiente_pivote(matriz=matriz, fila_inicio=i, col_inicio=j, n_cols_izq=n_izq)
    if fila_piv is None:
      solucion = False
      break

    if fila_piv != i:
      matriz = funciones.Intercambiar_filas(matriz=matriz, fila_base=i, fila_destino=fila_piv)
      pasos_inversa.append(copy.deepcopy(matriz))
      id_pasos_inversa.append([1, i, fila_piv])

    if matriz[i][col_piv] != 1:
      matriz[i], factor = funciones.Hacer_uno_pivote(fila=matriz[i], indice_columna=col_piv)
      pasos_inversa.append(copy.deepcopy(matriz))
      id_pasos_inversa.append([2, factor])

    if i != (len(matriz) - 1):
      matriz = funciones.Hacer_cero_abajo_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
      pasos_inversa.append(copy.deepcopy(matriz)); id_pasos_inversa.append([3, col_piv])

    if i != 0:
      matriz = funciones.Hacer_cero_arriba_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
      pasos_inversa.append(copy.deepcopy(matriz)); id_pasos_inversa.append([4, col_piv])

    i += 1
    j = col_piv + 1

  if not pasos_inversa or pasos_inversa[-1] is not matriz:
    pasos_inversa.append(copy.deepcopy(matriz)); id_pasos_inversa.append(["final"])

  return pasos_inversa, id_pasos_inversa, solucion

def obtener_inversa(matriz):
  if (validaciones.validar_matriz_cuadrada(matriz=matriz) == False):
    respuesta = ["Recuerda que para calcular la inversa de una matriz, esta matriz tiene que ser cuadrada, Amxm", 0, 0]
  else:
    tamaño = len(matriz)
    matriz_identidad = funciones.crear_matriz_identidad(tamaño=tamaño)
    matriz_unida = funciones.concatenar_matrices(matriz_izquierda=matriz, matriz_derecha=matriz_identidad)
    inversa, id_pasos, solucion = Gauss_Jordan_Inversa(matriz=matriz_unida, tamaño=tamaño)
    respuesta = ["La matriz original si tiene inversa", inversa, id_pasos] if solucion == True else ["La matriz no tiene inversa debido a que no todos los pivotes de la diagonal principal son 1", inversa, id_pasos]
  return respuesta
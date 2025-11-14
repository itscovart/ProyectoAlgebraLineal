"""
Funciones para calcular la inversa de una matriz usando el método de Gauss‑Jordan.
Se registra cada paso realizado para poder mostrar el procedimiento completo.
"""
import copy
from services import funciones, validaciones, determinante

"""
Aplica Gauss‑Jordan sobre la matriz aumentada [A|I] para obtener la inversa.
Input:
  matriz -> matriz aumentada [A|I]
  tamaño -> número de filas/columnas de A
Output:
  pasos_inversa -> lista de matrices intermedias
  id_pasos_inversa -> identificadores de cada operación realizada
  solucion -> True si la matriz es invertible, False si no
"""
def Gauss_Jordan_Inversa(matriz, tamaño):
  # Aquí almacenamos cada paso visual del proceso.
  pasos_inversa = []
  # Aquí registramos qué operación se realizó en cada paso (swap, pivote, ceros, etc.).
  id_pasos_inversa = []
  solucion = True

  # Número de columnas que pertenecen a A; los pivotes sólo se buscan ahí.
  n_izq = tamaño

  i = 0
  j = 0

  # Recorremos la matriz buscando pivotes fila por fila y columna por columna.
  while i < tamaño and j < n_izq:
    # Buscamos el siguiente pivote disponible a partir de la posición actual.
    fila_piv, col_piv = funciones.buscar_siguiente_pivote(matriz=matriz, fila_inicio=i, col_inicio=j, n_cols_izq=n_izq)
    # Si ya no hay pivotes, la matriz no es invertible.
    if fila_piv is None:
      solucion = False
      break

    # Si el pivote no está en la fila actual, intercambiamos filas para colocarlo arriba.
    if fila_piv != i:
      matriz = funciones.Intercambiar_filas(matriz=matriz, fila_base=i, fila_destino=fila_piv)
      pasos_inversa.append(copy.deepcopy(matriz))
      id_pasos_inversa.append([1, i, fila_piv])

    # Si el pivote no es 1, normalizamos la fila para convertirlo en 1.
    if matriz[i][col_piv] != 1:
      matriz[i], factor = funciones.Hacer_uno_pivote(fila=matriz[i], indice_columna=col_piv)
      pasos_inversa.append(copy.deepcopy(matriz))
      id_pasos_inversa.append([2, factor])

    # Eliminamos los valores debajo del pivote (hacer ceros hacia abajo).
    if i != (len(matriz) - 1):
      matriz = funciones.Hacer_cero_abajo_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
      pasos_inversa.append(copy.deepcopy(matriz)); id_pasos_inversa.append([3, i, col_piv])

    # Eliminamos los valores encima del pivote (hacer ceros hacia arriba).
    if i != 0:
      matriz = funciones.Hacer_cero_arriba_ij(matriz=matriz, fila_pivote=i, col_pivote=col_piv)
      pasos_inversa.append(copy.deepcopy(matriz)); id_pasos_inversa.append([4, i, col_piv])

    i += 1
    j = col_piv + 1

  # Añadimos el estado final de la matriz si aún no se ha registrado.
  if not pasos_inversa or pasos_inversa[-1] is not matriz:
    pasos_inversa.append(copy.deepcopy(matriz)); id_pasos_inversa.append(["final"])

  return pasos_inversa, id_pasos_inversa, solucion

"""
Función de alto nivel que verifica si la matriz es cuadrada,
construye [A|I] y llama a Gauss‑Jordan para obtener la inversa.
"""
def obtener_inversa(matriz):
  # Verificamos que la matriz sea cuadrada antes de intentar invertirla.
  if (validaciones.validar_matriz_cuadrada(matriz=matriz) == False):
    respuesta = ["Recuerda que para calcular la inversa de una matriz, esta matriz tiene que ser cuadrada, Amxm", 0, 0]
  else:
    tamaño = len(matriz)
    # Creamos la matriz identidad del mismo tamaño que A.
    matriz_identidad = funciones.crear_matriz_identidad(tamaño=tamaño)
    # Unimos A y la identidad para formar la matriz aumentada [A|I].
    matriz_unida = funciones.concatenar_matrices(matriz_izquierda=matriz, matriz_derecha=matriz_identidad)
    # Aplicamos Gauss‑Jordan para intentar obtener la inversa.
    inversa, id_pasos, solucion = Gauss_Jordan_Inversa(matriz=matriz_unida, tamaño=tamaño)
    # Dependiendo de si todos los pivotes pudieron ser 1, la matriz será o no invertible.
    respuesta = ["La matriz original si tiene inversa", inversa, id_pasos] if solucion == True else ["La matriz no tiene inversa debido a que no todos los pivotes de la diagonal principal son 1", inversa, id_pasos]
  return respuesta
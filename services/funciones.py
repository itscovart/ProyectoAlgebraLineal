# Funciones auxiliares para operaciones con matrices usadas en el proyecto de Álgebra Lineal.
# Incluye acciones para intercambiar filas, generar matrices identidad, separar matrices aumentadas
# y procesar soluciones de SEL.

import copy, math

"""
  Funcion para intercambiar filas de una matriz.
  Input: matriz, fila a cambiar, fila destino
  Output: Nueva matriz con filas intercambiadas.
"""
def Intercambiar_filas(matriz, fila_base, fila_destino) -> list:
  # copy.deepcopy crea una copia independiente de la matriz original (no la modifica).
  nueva_matriz = copy.deepcopy(matriz)
  # Guardamos temporalmente la fila base para poder intercambiarla.
  temp = nueva_matriz[fila_base]
  nueva_matriz[fila_base] = nueva_matriz[fila_destino]
  nueva_matriz[fila_destino] = temp
  return nueva_matriz

"""
  Funcion para normalizar una fila para que su pivote sea 1.
  Input: fila completa, indice del pivote
  Output: Nueva fila con pivote igual a 1 y factor original.
"""
def Hacer_uno_pivote(fila, indice_columna) -> list:
  # Creamos una copia de la fila para no modificar directamente la original.
  nueva_fila = fila.copy()
  # Calculamos el factor necesario para que el valor en la posicion del pivote se vuelva 1.
  pivote = 1/nueva_fila[indice_columna]
  factor = nueva_fila[indice_columna]
  # Recorremos cada elemento de la fila y lo multiplicamos por el factor del pivote.
  for i, valor in enumerate(nueva_fila):
    nueva_fila[i] = pivote * valor
  return nueva_fila, factor

"""
  Funcion para hacer ceros por debajo del pivote en la columna indicada.
  Usa la fila del pivote como referencia.
  Output: Nueva matriz con ceros debajo del pivote.
"""
def Hacer_cero_abajo_ij(matriz, fila_pivote, col_pivote) -> list:
  """
  Hace ceros por debajo en la columna col_pivote usando la fila fila_pivote como pivote.
  No asume pivote en a_ii.
  """
  # Trabajamos sobre una copia para no modificar la matriz original.
  nueva_matriz = copy.deepcopy(matriz)
  # m representa el numero total de filas de la matriz.
  m = len(nueva_matriz)
  # Si la fila del pivote es la ultima o no hay filas debajo, no hay nada que hacer.
  if fila_pivote >= m - 1:
    return nueva_matriz
  # Recorremos todas las filas que estan por debajo de la fila del pivote.
  for i in range(fila_pivote + 1, m):
    # Este valor indica cuanto hay que restar de la fila pivote para hacer cero esta posicion.
    factor = nueva_matriz[i][col_pivote]
    if factor != 0:
      # Recorremos todas las columnas de la fila actual para actualizar cada valor.
      for j in range(len(nueva_matriz[i])):
        nueva_matriz[i][j] -= factor * nueva_matriz[fila_pivote][j]
  return nueva_matriz

"""
  Funcion para hacer ceros por arriba del pivote en la columna indicada.
  Usa la fila del pivote como limite.
  Output: Nueva matriz con ceros arriba del pivote.
"""
def Hacer_cero_arriba_ij(matriz, fila_pivote, col_pivote) -> list:
  # Trabajamos sobre una copia para no modificar la matriz original.
  nueva_matriz = copy.deepcopy(matriz)
  # Si el pivote esta en la primera fila, no hay filas por encima para modificar.
  if fila_pivote <= 0:
    return nueva_matriz
  # Recorremos las filas que estan por encima de la fila del pivote.
  for i in range(0, fila_pivote):
    factor = nueva_matriz[i][col_pivote]
    if factor != 0:
      for j in range(len(nueva_matriz[i])):
        nueva_matriz[i][j] -= factor * nueva_matriz[fila_pivote][j]
  return nueva_matriz

"""
  Funcion para buscar el siguiente pivote recorriendo columnas y filas.
  Input: matriz, fila_inicio, col_inicio, numero de columnas del bloque izquierdo.
  Output: (fila_pivote, col_pivote) o (None, None) si no existe.
"""
def buscar_siguiente_pivote(matriz, fila_inicio, col_inicio, n_cols_izq):
  """
  Recorre columnas desde col_inicio y busca una fila >= fila_inicio con entrada != 0.
  Devuelve (fila_pivote, col_pivote) o (None, None) si ya no hay pivotes.
  """
  # Validamos que la matriz no este vacia antes de buscar un pivote.
  if not matriz or not matriz[0]:
    return None, None
  # Limitamos la busqueda de pivotes al bloque izquierdo (sin tocar la columna aumentada).
  num_cols = min(n_cols_izq, len(matriz[0]))
  num_filas = len(matriz)
  # Recorremos columnas y filas en orden para encontrar el primer elemento no nulo.
  for j in range(col_inicio, num_cols):
    for i in range(fila_inicio, num_filas):
      if matriz[i][j] != 0:
        return i, j
  return None, None
  
"""
  Funcion para concatenar horizontalmente dos matrices.
  Output: Nueva matriz con las columnas unidas.
"""
def concatenar_matrices(matriz_izquierda, matriz_derecha):
    # Hacemos copias de las matrices para evitar modificar las originales.
    matriz_izquierda = copy.deepcopy(matriz_izquierda)
    matriz_derecha = copy.deepcopy(matriz_derecha)
    # zip recorre ambas matrices fila por fila, y concatenamos cada par de filas.
    matriz_unida = [fila_izq + fila_der for fila_izq, fila_der in zip(matriz_izquierda, matriz_derecha)]
    return matriz_unida
    
"""
  Funcion para generar una matriz identidad con definicion
  aij <- 1 si i == j sino 0
  Output: Matriz cuadrada identidad
"""
def crear_matriz_identidad(tamaño):
  # Crea una matriz cuadrada donde solo hay 1 en la diagonal principal.
  matriz_identidad = [[1 if i == j else 0 for j in range(tamaño)] for i in range(tamaño)]
  return matriz_identidad

"""
  Funcion para separar una matriz aumentada [A|b].
  Output: (matriz de coeficientes A, vector columna b).
"""
def separar_matriz_aumentada(matriz):
  # Tomamos todas las columnas excepto la ultima para formar la matriz de coeficientes A.
  coeficientes = copy.deepcopy([fila[:-1] for fila in matriz])
  # Tomamos solo la ultima columna de cada fila para formar el vector b como columna.
  igualdades = copy.deepcopy([[fila[-1]] for fila in matriz])
  return coeficientes, igualdades

"""
  Funcion para obtener la solucion de un SEL usando columnas pivote.
  Variables pivote se expresan en funcion de variables libres.
  Variables libres no se muestran.
  Output: diccionario de soluciones o mensaje de inconsistencia.
"""
def procesar_solucion_sel_por_pivotes(matriz, pivot_cols):

  # Verificamos si el sistema es inconsistente (fila de ceros con término independiente no nulo).
  inconsistencia, fila_inconsistencia = validar_incosistencia_sel(matriz=matriz)
  if inconsistencia:
    return f"El sistema tiene conjunto solución vacío por inconsistencia en la ecuación {fila_inconsistencia + 1}"

  # Separamos la matriz aumentada en matriz de coeficientes y vector de igualdades.
  coeficientes, igualdades = separar_matriz_aumentada(matriz=matriz)
  if not coeficientes:
    return [{}, 0]

  n = len(coeficientes[0])

  # Usamos una comprension de conjunto para quedarnos solo con las columnas que realmente son pivote.
  pivot_set = {c for c in pivot_cols if c is not None}
  # Las columnas que no estan en pivot_set representan variables libres.
  free_cols = [j for j in range(n) if j not in pivot_set]

  solucion = {}

  # Para cada fila de pivote, expresamos la variable pivote v_{col_pivote+1}
  # en función de las variables libres.
  for fila_idx, col_pivote in enumerate(pivot_cols):
    # Si esta fila no tiene pivote, la ignoramos.
    if col_pivote is None:
      continue
    # Validamos que el indice de la columna pivote este dentro del rango valido.
    if col_pivote < 0 or col_pivote >= n:
      continue

    # Tomamos el valor del lado derecho de la ecuacion (termino independiente).
    valor_igualdad = igualdades[fila_idx][0]   # término independiente
    valor_variable = f"{valor_igualdad}"

    # Recorremos las variables libres para expresar la variable pivote en funcion de ellas.
    for j in free_cols:
      # coef es el valor de la matriz en la fila del pivote y la columna de la variable libre.
      coef = coeficientes[fila_idx][j]
      if coef == 0:
        continue

      # Segun el signo del coeficiente, restamos o sumamos el termino al pasar al otro lado de la ecuacion.
      signo = " - " if coef > 0 else " + "
      # Usamos el valor absoluto para mostrar solo la magnitud numerica (sin signo).
      magnitud = abs(coef)
      # Si la magnitud es 1, no mostramos el numero explicitamente (solo la variable).
      if magnitud == 1:
        coef_str = ""
      else:
        coef_str = f"{magnitud}"

      valor_variable += f"{signo}{coef_str}v{j + 1}"

    solucion[f"v{col_pivote + 1}"] = valor_variable

  return solucion

"""
  Funcion para crear un diccionario a partir de listas de claves y valores.
  Output: diccionario clave->valor.
"""
def obtener_dict_valores_sel(claves, valores):
  # zip permite recorrer las dos listas al mismo tiempo para construir el diccionario.
  solucion = {}
  for k, v in zip(claves, valores):
      solucion[k] = v
  return solucion

"""
  Funcion para detectar inconsistencia en un SEL.
  Revisa filas tipo [0...0 | b] con b != 0.
  Output: [True, fila] si hay inconsistencia; [False, 0] si no.
"""
def validar_incosistencia_sel(matriz):
  # Recorremos cada fila para revisar si es una posible fila inconsistente.
  resultado = [False, 0]
  for i, fila in enumerate(matriz):
    # all(...) verifica que todos los coeficientes sean 0, y luego comprobamos que el termino independiente no sea 0.
    if all(valor == 0 for valor in fila[:-1]) and fila[-1] != 0:
      resultado = [True, i]
      break
  return resultado

def normalizar_matriz(matriz):
    matriz_normalizada = []
    for fila in matriz:
        fila_normalizada = []
        for x in fila:
            if isinstance(x, float) and x.is_integer():
                fila_normalizada.append(int(x))
            else:
                fila_normalizada.append(x)
        matriz_normalizada.append(fila_normalizada)
    return matriz_normalizada

def matrices_iguales(m1, m2, tol=1e-9):
    for f1, f2 in zip(m1, m2):
        for x, y in zip(f1, f2):
            if not math.isclose(x, y, abs_tol=tol):
                return False
    return True
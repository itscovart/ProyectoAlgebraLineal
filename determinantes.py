import numpy as np
from validacion_matriz import existenciaConjuntosPurosCeros

def resolverDeterminante(matriz):
  filas = len(matriz)
  matrizTranspuesta = np.array(matriz).T
  columnas = len(matrizTranspuesta)
  ## Validar si existen filas o columnas completas de puros ceros
  if(existenciaConjuntosPurosCeros(matriz=matriz) != filas or
     existenciaConjuntosPurosCeros(matriz=matrizTranspuesta) != columnas):
    print("El determinante de la matriz es 0, debido a que existe una fila o columna de puros ceros")
    exit(0)
  
import copy
from services import funciones, validaciones, determinante

def Gauss_Jordan_Inversa(matriz, tamaño):
  pasos_inversa = []
  id_pasos_inversa = []
  solucion = True
  
  for i, fila in enumerate(matriz):
    pivote = matriz[i][i]
    if(pivote == 0):
      indice_pivote_nuevo = funciones.encontrar_pivote_nuevo(matriz=matriz, indice_inicial=i)
      if(indice_pivote_nuevo == i):
        solucion = False
        break
      else:
        matriz = funciones.Intercambiar_filas(matriz=matriz, fila_base=i, fila_destino=indice_pivote_nuevo)
        pasos_inversa.append(copy.deepcopy(matriz))
        id_pasos_inversa.append([1, i, indice_pivote_nuevo])
        pivote = matriz[i][i]
        
    elif(pivote != 1):
      matriz[i], factor = funciones.Hacer_uno_pivote(fila=fila, indice_columna=i)
      pasos_inversa.append(copy.deepcopy(matriz))
      id_pasos_inversa.append([2, factor])
      
    matriz = funciones.Hacer_cero_abajo(matriz=matriz, indice_pivote=i)
    pasos_inversa.append(copy.deepcopy(matriz))
    id_pasos_inversa.append([3])
    matriz = funciones.Hacer_cero_arriba(matriz=matriz, indice_pivote=i)
    pasos_inversa.append(copy.deepcopy(matriz))
    id_pasos_inversa.append([4])
      
  return pasos_inversa, id_pasos_inversa, solucion

def obtener_inversa(matriz):
  if(determinante.obtener_determinante(matriz=matriz) == False):
    respuesta = ["La matriz tiene como determinante 0 por lo tanto no es una matriz invertible", 0, 0]
  elif (validaciones.validar_matriz_cuadrada(matriz=matriz) == False):
    respuesta = ["Recuerda que para calcular la inversa de una matriz, esta matriz tiene que ser cuadrada, Amxm", 0, 0]
  else:
    tamaño = len(matriz)
    matriz_identidad = funciones.crear_matriz_identidad(tamaño=tamaño)
    matriz_unida = funciones.concatenar_matrices(matriz_izquierda=matriz, matriz_derecha=matriz_identidad)
    inversa, id_pasos, solucion = Gauss_Jordan_Inversa(matriz=matriz_unida, tamaño=tamaño)
    respuesta = ["La matriz original si tiene inversa", inversa, id_pasos] if solucion == True else ["La matriz no se pudo resolver debido a que no se encontraron mas pivotes distinto de 0", inversa, id_pasos]
  return respuesta
  
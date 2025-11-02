import copy
from services import funciones, validaciones

def gauss_jordan_sel(coeficientes, igualdades):
  pasos_sel = []
  id_pasos = []
  solucion = [True]
  matriz_unida = funciones.concatenar_matrices(matriz_izquierda=coeficientes, matriz_derecha=igualdades)
  for i, fila in enumerate(coeficientes):
    pivote = matriz_unida[i][i]
    if(pivote == 0):
      nuevo_indice = funciones.encontrar_pivote_nuevo(matriz=matriz_unida, indice_inicial=i)
      
      if(nuevo_indice == i):
        solucion = [False, i]
        break
      
      else:
        matriz_unida = funciones.Intercambiar_filas(matriz=matriz_unida, fila_base=i, fila_destino=nuevo_indice)
        pasos_sel.append(copy.deepcopy(matriz_unida))
        id_pasos.append([1, i, nuevo_indice])
        pivote = matriz_unida[i][i]
        
    if(pivote != 1):
      matriz_unida[i], factor = funciones.Hacer_uno_pivote(fila=matriz_unida[i], indice_columna=i)
      pasos_sel.append(copy.deepcopy(matriz_unida))
      id_pasos.append([2, factor])
    
    matriz_unida = funciones.Hacer_cero_abajo(matriz=matriz_unida, indice_pivote=i)
    pasos_sel.append(copy.deepcopy(matriz_unida))
    id_pasos.append([3])
    matriz_unida = funciones.Hacer_cero_arriba(matriz=matriz_unida, indice_pivote=i)
    pasos_sel.append(copy.deepcopy(matriz_unida))
    id_pasos.append([4])
    
  solucion = funciones.procesar_solucion_sel(solucion, matriz_unida)
    
  return solucion, pasos_sel, id_pasos
def resolver_matriz(matriz):
  if(validaciones.validar_tamaño_minimo_sel(matriz=matriz)):
    coeficientes, igualdades = funciones.separar_matriz_aumentada(matriz=matriz)
    solucion, matriz_pasos, id_matriz_pasos = gauss_jordan_sel(coeficientes=coeficientes, igualdades=igualdades)
    resultado = [solucion, matriz_pasos, id_matriz_pasos]
  else:
    resultado = ["La matriz no cumple con el tamaño minimo para poder resolver un sistema de ecuaciones que es de 1x2", 0, 0]
  return resultado
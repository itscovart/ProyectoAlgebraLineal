from funciones import Intercambiar_filas, Hacer_uno_pivote, Hacer_cero_abajo, Hacer_cero_arriba

def Gauss_Jordan(matriz, filas) -> list:
  for i, fila in enumerate(matriz):
    ## Verificar si el pivote es =
    if(matriz[i][i] == 0):
      contador = i + 1
      ## Encontrar fila con un elemento en la columna del pivote distinto de 0
      while(contador < filas and matriz[contador][i] == 0):
        contador += 1
      ## Cambiar filas en caso de haber una sin un 0
      Intercambiar_filas(matriz, i, contador - 1)
    ## Caso donde el pivote ya no es 0
    matriz[i] = Hacer_uno_pivote(fila, i)
    matriz = Hacer_cero_abajo(matriz, i)
    matriz = Hacer_cero_arriba(matriz, i)
  return matriz
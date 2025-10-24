
#Imprmir la matriz
#Funcion para imprimir con formato adecuado la matriz resultante
def imprimir_matriz(matriz:list):
    print("\n")
    for fila in matriz:
        print(", ".join(f"{x:6.2f}" for x in fila))

#Cambiar filas
def cambiar_filas(matriz: list, indice_fila_1: int, indice_fila_2:int) -> list:
    if indice_fila_1 == indice_fila_2:# valida que las filas que se vaya a intervambiar no sean las mismas
        return None
    
    matriz[[indice_fila_1, indice_fila_2]] = matriz[[indice_fila_2, indice_fila_1]]
    
    imprimir_matriz(matriz)
    print(f"\nR{indice_fila_1+1} -> R{indice_fila_2+1}")
    print(f"R{indice_fila_2+1} -> R{indice_fila_1+1}")
    
    return matriz

#Posiciones tentativas
#son todas la posiciones en donde se encuentran los pivotes (sin importar su valor) dentro de la matriz donde i = j
def posiciones_tentativas(n_filas:int,n_columnas:int)->list:# devuelve un arreglo con elementos k donde k=i=j
    posiciones = []
    if n_filas < n_columnas:
        p = n_filas
    else:
        p = n_columnas

    for i in range(p):
        posiciones.append(i)
        
    return posiciones

#Escoger pivote
#verifica el pivote, lo escoge y coloca el pivote en la posicion a(ii)
def escoger_pivote(matriz:list, posicion_tentativa:tuple, n_filas: int) -> tuple:
    #escoger la fila y columna del pivote
    posicion_pivote = (-1,-1)
    fila_pivote = posicion_tentativa[0]
    columna_actual = posicion_tentativa[1] 

    for i in range(n_filas):
        if matriz[i][columna_actual] != 0:
            cambiar_filas(matriz,fila_pivote,i)
            posicion_pivote = (i,columna_actual)
            break

    return posicion_pivote# si no encuentra pivote devolverá (-1,-1)

#Hacer 1 en pivote
#dividir la fila donde esta el pivote entre el pivote
def Hacer_uno_pivote(matriz: list, pos_pivote:tuple) -> list:
  pivote = matriz[pos_pivote[0],pos_pivote[1]]
  matriz[pos_pivote[0]] *= 1/pivote
  
  imprimir_matriz(matriz)
  print(f"\nR{pos_pivote[0]+1} * 1/{pivote} -> R{pos_pivote[0]+1}")
  
  return matriz

#Hacer 0's abajo del pivote
def ceros_abajo(matriz:list,posicion_pivote:tuple, n_filas:int) -> list:
    fila_pivote = posicion_pivote[0]
    columna_pivote = posicion_pivote[1]
    #revisa primero que hayan ceros abajos para convertir
    if fila_pivote == n_filas-1:
        return None
    
    for i in range(fila_pivote+1,n_filas):
        k = matriz[i, columna_pivote]
        matriz[i] = matriz[i] -(k*matriz[fila_pivote])
        
        imprimir_matriz(matriz)
        print(f"\nR{i+1} {-1*k:+}R{fila_pivote+1} -> R{i+1}")

    return matriz

#Hacer 0's arriba del pivote
def ceros_arriba(matriz:list,posicion_pivote:tuple, n_filas:int) -> list:
    fila_pivote = posicion_pivote[0]
    columna_pivote = posicion_pivote[1]
    #revisa primero que hayan ceros arriba para convertir
    if fila_pivote == 0:
        return None
    
    for i in range(fila_pivote-1,-1,-1):
        k = matriz[i, columna_pivote]
        matriz[i] = matriz[i] -(k*matriz[fila_pivote])

        imprimir_matriz(matriz)
        print(f"\nR{i+1} {-1*k:+}R{fila_pivote+1} -> R{i+1}")

    return matriz






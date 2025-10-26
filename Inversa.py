import numpy as np
import FuncionesGJ as fgj
import Validaciones as val

#matriz de prueba
matriz = [
    [1,2,-1,4],
    [2,1,1,5],
    [-1,3,2,1]
]

matriz = np.array(matriz)
matriz = matriz.astype(float)#.astype ya valida que todos los elementos de la matriz sean flotantes
n_filas = len(matriz)
n_columnas = len(matriz[0])


#validar si una matriz es cuadrada
def verificar_matriz_cuadrada(matriz: list) -> bool:
    #Comprobamos que tenga el mismo número de filas y columnas
    filas, columnas = len(matriz),len(matriz[0])
    if filas == columnas:
        return True
    else:
        print(f"La matriz tiene un tamaño {filas} x {columnas}. Por lo tanto no es cuadrada.")
        return False

#Generar una matriz identidad de tamaño n x n.
def matriz_identidad(n: int) -> list:
    identidad = np.eye(n, dtype=float)

    print(identidad)
    return identidad

#Genera la matriz aumentada
def matriz_aumentada(matriz: list, identidad: list) -> list:#recibe una matriz cuadrada y su identidad y devuelve la matriz aumentada
    # Concatenación horizontal [A | I]
    aumentada = np.concatenate((matriz, identidad), axis=1)

    print(aumentada)
    return aumentada

def gauss_jordan_inv(matriz:list, n_filas:int, n_columnas:int) -> list:
    #Validaciones generales
    if not val.validar_n_columnas_filas(matriz,n_columnas):
        return None
    if not verificar_matriz_cuadrada(matriz):
        return None
    
    #concatenar matriz con su identidad
    identidad = matriz_identidad(n_filas)
    matriz = matriz_aumentada(matriz,identidad)


    posiciones = fgj.posiciones_tentativas(n_filas,n_columnas)
    for k in range(n_columnas):


        print(f"\n------Columna {k+1}------")
        p = posiciones[k] 
        pivote=(p,p)#donde i = j
        if matriz[p][p] == 0:
            pivote = fgj.escoger_pivote(matriz,p,n_filas)
            if pivote == (-1,-1):#significa que no hay pivote en la columna y se pasa a la siguiente
                continue
        
        fgj.Hacer_uno_pivote(matriz,pivote)
        fgj.ceros_abajo(matriz,pivote,n_filas)
        fgj.ceros_arriba(matriz,pivote,n_filas)

    #dividir y mostrar la matriz resultante, nota: validar tambien si su determinante es != 0
    A1, inversa = np.hsplit(matriz, 2)
    print(f"\n------Matriz inversa------")
    fgj.imprimir_matriz(inversa)
    print("\n")


gauss_jordan_inv(matriz,n_filas,n_columnas)



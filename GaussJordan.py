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

#Gauss jordan
print(matriz)

#Validaciones generales
val.validar_n_columnas_filas(matriz,n_columnas)
val.inconsistencia(matriz,n_columnas)


posiciones = fgj.posiciones_tentativas(n_filas,n_columnas)
for k in range(n_columnas-1):
    #validaciones por iteracion
    if val.inconsistencia(matriz,n_columnas):
        break

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

#validaciones de la matriz resultante
val.inconsistencia(matriz,n_columnas)
val.filas_puros_ceros(matriz)


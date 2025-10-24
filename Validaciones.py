import numpy as np

# Validamos que las filas no tengan cantidad de columnas distintas
def validar_n_columnas_filas(matriz:list, n_columnas:int) -> bool:
    for fila in matriz:
        if len(fila) != n_columnas:
            print("Error. Cantidad de columnas distintas.")
            return False
    print("Dimensiones correctas.")
    return True

# Validamos si el sistema no tiene solucion
def inconsistencia(matriz:list, n_columnas:int) -> bool:
    for n, fila in enumerate(matriz):
        # Revisar si todos los coeficientes (menos la última columna) son cero
        if all(valor == 0 for valor in fila[:n_columnas-1]):
            # Verificar si el término independiente no es cero
            if fila[n_columnas-1] != 0:
                print(f"Existe una inconsistencia en la fila {n+1}. Por lo tanto la matriz no tiene solución.")
                return True
    return False

#En caso de ser un sistema con infitas soluciones calculan las variables libres
def variables_libres(matriz:list,n_columnas:int):
    matriz = np.array(matriz)

    filas_cero = np.all(matriz == 0, axis=1)#validar si cada fila está llena de ceros
    cantidad = np.sum(filas_cero)#sumar cuantas filas de 0s hubo

    #agregar todas la varaivles libres en una lista
    var_libres=list(range(n_columnas-cantidad,n_columnas))
    
    #imprimir las variables libres
    print(f"\nVariables libres: ",end="")
    for i in var_libres:
        print(f"x{i}",end=", ")
    print("\n")

# Validamos si el sistema tiene infinitas soluciones (fila de puros 0s)
def filas_puros_ceros(matriz:list):
    for n, fila in enumerate(matriz):
        # Verificar si todos los elementos son cero
        if all(valor == 0 for valor in fila):
            print(f"La fila {n + 1} es de puros 0s")





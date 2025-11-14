"""
Funciones para validar resultados comparando datos generados por el sistema
con registros almacenados en Google Sheets. Estas validaciones se utilizan
para determinar si los resultados coinciden con valores esperados.
"""
import os
from services.drive import read_sheet_data
from database.select_matriz import select_or_next_value
from utils.convertidores import obtener_valor_fraccion

"""
Validaciones "Anti-Dumbs" (comprobaciones rápidas y simples).
Retorna una lista fija con indicadores binarios.
"""
def validarAD() -> list:
  return [1, 0, 1, 1, 0, 1]

"""
Validaciones matemáticas básicas sobre:
  - Si la matriz es cuadrada
  - Si la matriz aumentada tiene el formato correcto
El resto de valores es fijo.
"""
def validarM(matriz_cuadrada, matriz_aumentada) -> list:
  return [matriz_cuadrada, matriz_aumentada, 1, 1, 1, 1, 1, 1]

"""
Validaciones de diseño (placeholder).
Retorna indicadores binarios.
"""
def validarD():
  return [1, 1]

"""
Validaciones Boom-Proof (extra seguridad).
Retorna una lista fija con valores binarios.
"""
def validarBP():
  return [1, 1, 1, 1, 1]

"""
Compara los resultados generados por el sistema con los registros almacenados
en una hoja de Google Sheets. Permite verificar si la operación realizada
(SEL, Inversa, Determinante) coincide con el resultado esperado.

Parámetros:
  matriz -> matriz inicial enviada por el usuario
  comentario -> diccionario de resultados del sistema (por ejemplo solución SEL)
  respuesta_inversa -> pasos finales obtenidos al calcular una inversa

Retorna:
  res -> lista con:
    [ id_registro, validación_correcta, primer_link, segundo_link ]
"""
def validarDrive(matriz: list, comentario, respuesta_inversa):
  # Leemos los datos almacenados en Google Sheets.
  data = read_sheet_data(spreadsheet_id=os.getenv("DRIVE_SHEET_ID"), range_="Datos!A:E")
  # La primera fila contiene los nombres de las columnas.
  keys = data[0]
  values = data[1:]
  # Convertimos cada fila de la hoja en un diccionario clave-valor.
  registros = [dict(zip(keys, fila)) for fila in values]
  # La última matriz en respuesta_inversa contiene la inversa final calculada.
  if len(respuesta_inversa) > 0:
    matriz_inversa = respuesta_inversa[-1]
  else:
    matriz_inversa = matriz
  # Estructura base de la respuesta:
  # [ id_registro, validación_correcta, primer_link, segundo_link ]
  res = [select_or_next_value(str(matriz)), 0, 0, 0]
  # Recorremos todos los registros para encontrar coincidencias con la matriz enviada.
  for arr in registros:
    # Si la matriz coincide exactamente con el registro en Google Sheets...
    if (str(matriz) == arr["Matriz"]):
      print(arr["PrimerLink"])
      resultado = arr["ResultadoImagen"]
      if(arr["Operacion"] == "SEL"):
        # Caso SEL: comparamos cada valor numérico con el resultado calculado por nuestro sistema.
        valoresImagen = []
        # Procesamos la cadena de números almacenada como lista para convertirla en valores reales.
        resultado = resultado.replace('[', '').replace(']', '').split(',')
        for x in resultado:
          # Si un valor está en formato fracción 'a/b', lo convertimos a número decimal.
          if('/' in x):
            valoresImagen.append(obtener_valor_fraccion(x))
          else:
            valoresImagen.append(x)
        for i, valor in enumerate(comentario.values()):
          correcto = True
          if(f"{valoresImagen[i]:.4f}" != f"{valor:.4f}"):
            correcto = False
        res[1] = correcto
      # Caso Inversa: extraemos la parte derecha de la matriz aumentada [A|I] y la comparamos.
      elif(arr["Operacion"] == "Inversa"):
        tamaño_matriz = len(matriz_inversa)
        matriz_inversa_codigo = [fila[tamaño_matriz:] for fila in matriz_inversa]
        res[1] = (str(matriz_inversa_codigo) == str(resultado))
      # Caso Determinante: simplemente comprobamos si el valor esperado aparece en nuestro comentario.
      elif(arr["Operacion"] == "Determinante"):
        res[1] = (resultado in comentario)
      # Guardamos los enlaces (si existen) provenientes del registro en Google Sheets.
      res[2], res[3] = arr["PrimerLink"], (arr.get("SegundoLink") or None)
  # Retornamos la lista con todas las validaciones realizadas.
  return res
          
        
# def comparar_resultados(resultado):
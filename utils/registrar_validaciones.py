import os
from services.drive import read_sheet_data
from database.select_matriz import select_or_next_value
from utils.convertidores import fraction_number

def validarAD() -> list:
  return [1, 0, 1, 1, 0, 1]

def validarM(matriz_cuadrada, matriz_aumentada, valido) -> list:
  return [matriz_cuadrada, matriz_aumentada, 1, 1, 1, 1, 1, 1] if valido else [0, 0, 0, 0, 0, 0, 0, 0]

def validarD():
  return [1, 1]

def validarBP():
  return [1, 1, 1, 1, 1]

def validarDrive(matriz: list, comentario, respuesta_inversa):
  data = read_sheet_data(spreadsheet_id=os.getenv("DRIVE_SHEET_ID"), range_="Datos!A:E")
  keys = data[0]
  values = data[1:]
  registros = [dict(zip(keys, fila)) for fila in values]
  matriz_inversa = respuesta_inversa[-1]
  res = [select_or_next_value(str(matriz)), 0, 0, 0]
  for arr in registros:
    if (str(matriz) == arr["Matriz"]):
      print(arr["PrimerLink"])
      resultado = arr["ResultadoImagen"]
      if(arr["Operacion"] == "SEL"):
        valoresImagen = []
        resultado = resultado.replace('[', '').replace(']', '').split(',')
        for x in resultado:
          if('/' in x):
            valoresImagen.append(fraction_number(x))
          else:
            valoresImagen.append(x)
        for i, valor in enumerate(comentario.values()):
          correcto = True
          if(f"{valoresImagen[i]:.4f}" != f"{valor:.4f}"):
            correcto = False
        res[1] = correcto
      elif(arr["Operacion"] == "Inversa"):
        tamaño_matriz = len(matriz_inversa)
        matriz_inversa_codigo = [fila[tamaño_matriz:] for fila in matriz_inversa]
        res[1] = (str(matriz_inversa_codigo) == str(resultado))
      elif(arr["Operacion"] == "Determinante"):
        res[1] = (resultado in comentario)
      res[2], res[3] = arr["PrimerLink"], (arr.get("SegundoLink") or None)
  return res
          
        
# def comparar_resultados(resultado):
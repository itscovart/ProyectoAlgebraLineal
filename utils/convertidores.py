"""
Convierte una fracción en forma de string 'a/b' a un número decimal (float).
Input:
  number -> string con formato 'a/b'
Output:
  float(a) / float(b)
"""
def obtener_valor_fraccion(number):
  # Separamos el numerador y el denominador usando '/' como delimitador.
  a, b = number.split('/')
  # Convertimos ambos valores a float y realizamos la división.
  return float(a) / float(b)
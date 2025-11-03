# Calculadora de Matrices
Una API creada con FastAPI capaz de realizar operaciones de matrices (Determinantes, Inversa, Sistema de Ecuaciones Lineales) utilizando únicamente Gauss - Jordan

Este proyecto fue creado como proyecto para la asignatura de Álgebra Lineal en la carrera de Inteligencia Artificial impartida en ESCOM escuela perteneciente al IPN en México
Permite subir matrices como archivos y obtener el resultado correspondiente a la operación solicitada

## Tabla de contenido
- [Instalación](#instalación)
- [Ejemplos de API](#ejemplos-de-api)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)
- [Licencia](#licencia)

## Instalación

1. Clona el repositorio
  git clone https://github.com/itscovart/ProyectoAlgebraLineal.git

2. Entra al directorio
```bash
  cd ProyectoAlgebraLineal
```

3. Crea un entorno virtual e instala dependencias
```bash
  python -m venv venv
  source venv/bin/activate  # En macOS/Linux
  venv\Scripts\activate     # En Windows
  pip install -r requirements.txt
```

4. Ejecuta el servidor
```bash
  uvicorn main:app --reload
```

5. Abre el navegador
```bash
  http://127.0.0.1:8000/docs
```

## Ejemplo de API
El servidor espera un FormData con un archivo con extensión .txt y un campo de texto con el nombre de la operación a realizar:
  - "Determinante"
  - "Inversa"
  - "SEL" #Sistema de Ecuaciones Lineales
```bash
curl -X POST -F "file=@matriz.txt" -F "operacion=Determinante" http://127.0.0.1:8000/matrices/procesar
```

El servidor responde con un JSON con el siguiente formato:
```json
{
  "operacion": "La operación que se solicitó",
  "matriz_inicial": "Matriz inicial",
  "comentario": "Solución o texto con observaciones",
  "matrices_pasos": "Transformación de la matriz inicial a través de cada paso para ver cómo fue cambiando según la operación",
  "matrices_pasos_id": "El arreglo de las operaciones que se fueron realizando para llegar al resultado"
}

```

## Operaciones matrices_pasos_id
Arreglo devuelto:
```python
- [1, indice_de_origen, indice_de_destino] # Intercambio de filas
- [2, factor_que_se_factorizo] # Hacer uno el pivote
- [3] # Hacer ceros abajo
- [4] # Hacer ceros arriba
```

## Estructura del proyecto
```bash
app/
├── routes/
├── services/
├── utils/
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```


## Tecnologías
- Python 3.11
- FastAPI
- Uvicorn

## Licencia
Este proyecto está bajo la licencia MIT - consulta del archivo [LICENSE](LICENSE) para más detalles.
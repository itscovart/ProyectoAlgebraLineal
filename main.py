"""
Archivo principal de la API desarrollada con FastAPI.
Define la aplicación, configura CORS y registra las rutas del proyecto.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import matrices, foto

# Creamos la aplicación principal de FastAPI con título y versión.
app = FastAPI(title="API para resolver matrices con Gauss-Jordan", version="1.0")

# Dominios permitidos para realizar peticiones al backend (CORS).
origins = [
    "http://localhost:5173",
    "http://localhost", 
    "https://frontendlineal-production.up.railway.app",
    "http://192.168.100.46:5173",
    "https://solumatrix.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    # Permitimos peticiones solo desde los dominios definidos anteriormente.
    allow_origins=origins,       
    # Permitimos el envío de cookies/autenticación si fuera necesario.
    allow_credentials=True,
    # Permitimos todos los métodos HTTP (GET, POST, PUT, DELETE, etc.).
    allow_methods=["*"],        
    # Permitimos cualquier encabezado personalizado en la petición.
    allow_headers=["*"],        
)

# Registramos las rutas del módulo de matrices.
app.include_router(matrices.router, prefix="/matrices", tags=["Matrices"])
# Registramos las rutas del módulo de foto (subida y registro de imágenes).
app.include_router(foto.router, prefix="/foto", tags=["Foto"])

"""
Endpoint raíz para verificar que la API está funcionando correctamente.
"""
@app.get('/')
def root():
  # Respondemos con un mensaje simple para pruebas rápidas.
  return{
    "message": "API funcionando corrrectamente"
  }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import matrices

app = FastAPI(title="API para resolver matrices con Gauss-Jordan", version="1.0")
origins = [
    "http://localhost:5173",
    "http://localhost", 
    "https://frontendlineal-production.up.railway.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],        
)

app.include_router(matrices.router, prefix="/matrices", tags=["Matrices"])

@app.get('/')
def root():
  return{
    "message": "API funcionando corrrectamente"
  }
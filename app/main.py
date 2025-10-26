from fastapi import FastAPI
from routes import matrices

app = FastAPI(title="API para resolver matrices con Gauss-Jordan", version="1.0")

app.include_router(matrices.router, prefix="/matrices", tags=["Matrices"])

@app.get('/')
def root():
  return{
    "message": "API funcionando corrrectamente"
  }
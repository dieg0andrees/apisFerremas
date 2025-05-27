from fastapi import FastAPI
from usuarios.routes import usuarios, pedidos, producto_pedidos

app = FastAPI(
    title="API de gestion de usuarios para Ferramas",
    version="1.0.0",
    description="Api para la gestion de los usuarios de la empresa Ferramas, usando FastAPI y Oracle como base de datos"
)

app.include_router(usuarios.router)
app.include_router(pedidos.router)
app.include_router(producto_pedidos.router)
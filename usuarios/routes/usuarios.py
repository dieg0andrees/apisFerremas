from fastapi import APIRouter, HTTPException
from usuarios.database import get_conexion

router = APIRouter(
    prefix="/usuarios",
    tags= ["Usuarios"]
)

#Aqui comienzo a hacer los endpoints


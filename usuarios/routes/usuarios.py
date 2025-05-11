from fastapi import APIRouter, HTTPException
from usuarios.database import get_conexion

router = APIRouter(
    prefix="/usuarios",
    tags= ["Usuarios"]
)

#Aqui comienzo a hacer los endpoints
@router.get("/")
def obtener_usuarios():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT
            usuarios.RUT_USER,
            usuarios.NOMBRE_USER,
            usuarios.P_APELLIDO,
            usuarios.S_APELLIDO,
            usuarios.CORREO_USER,
            usuarios.CONTRASENA_USER,
            GENERO.DESCRIPCION,
            ROL.DESCRIPCION
        FROM usuarios
        join GENERO on usuarios.ID_GENERO = GENERO.ID_GENERO
        join rol on usuarios.ID_ROL = ROL.ID_ROL
        """)
        usuarios = []

        for rut_user, nombre, p_apellido, s_apellido, correo_user, contrasena_user, genero, rol in cursor:
            usuarios.append({
                "rut":rut_user,
                "nombre": nombre,
                "primer_apellido":p_apellido,
                "segundo_apellido":s_apellido,
                "correo_usuario":correo_user,
                "contrasena_usuario":contrasena_user,
                "genero": genero,
                "rol": rol
            })
        cursor.close()
        cone.close()
        return usuarios
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

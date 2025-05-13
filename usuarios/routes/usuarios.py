from fastapi import APIRouter, HTTPException
from usuarios.database import get_conexion

router = APIRouter(
    prefix="/usuarios",
    tags= ["Usuarios"]
)

#Aqui comienzo a hacer los endpoints
#Primer Get: obtener todos los usuarios
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
    
#Segundo Get: Usuario a buscar por rut
@router.get("/{rut_buscar}")
def obtener_usuario(rut_buscar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT            
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
        where rut_user =: rut """
        ,{"rut": rut_buscar})
        
        usuario = cursor.fetchone()
        cursor.close()
        cone.close()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no Encontrado")
        return{
            "rut":rut_buscar,
            "nombre": usuario[0],
            "primero_apellido": usuario[1],
            "segundo_apellido": usuario[2],
            "correo_usuario": usuario[3],
            "contrasena_usuario": usuario[4],
            "genero": usuario[5],
            "rol": usuario[6]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


#Post: Agregar usuarios
@router.post("/")
def agregar_usuario(rut_user:str, nombre_user:str, p_apellido:str, s_apellido:str, correo_user:str, contrasena_user:str, id_genero:int, id_rol:int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute(
            """
            insert into usuarios 
            values(
            :rut_user, 
            :nombre_user, 
            :p_apellido, 
            :s_apellido, 
            :correo_user, 
            :contrasena_user, 
            :id_genero, 
            :id_rol)
            """, {"rut_user":rut_user, 
                  "nombre_user":nombre_user, 
                  "p_apellido":p_apellido, 
                  "s_apellido":s_apellido , 
                  "correo_user":correo_user, 
                  "contrasena_user":contrasena_user, 
                  "id_genero":id_genero, 
                  "id_rol":id_rol})
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario agregado con exito"}    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
#Put: Actualizar usuarios
@router.put("/{rut_actualizar}")
def actuliazar_usuario(rut_actualizar:str, nombre_user:str, p_apellido:str, s_apellido:str, correo_user:str, contrasena_user:str, id_genero:int, id_rol:int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute(
        """
        update usuarios
        set 
        nombre_user = :nombre_user, 
        p_apellido = :p_apellido, 
        s_apellido = :s_apellido, 
        correo_user = :correo_user,
        contrasena_user = :contrasena_user,
        id_genero = :id_genero, 
        id_rol = :id_rol
        where rut_user = :rut 
        """, {"rut":rut_actualizar, 
              "nombre_user":nombre_user, 
              "p_apellido":p_apellido, 
              "s_apellido":s_apellido, 
              "correo_user":correo_user, 
              "contrasena_user":contrasena_user, 
              "id_genero":id_genero, 
              "id_rol":id_rol})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no Encontrado")
        
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario actualizado correctamente"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
#Delete: Eliminar Usuarios
@router.delete("/{rut_eliminar}")
def eliminar_usuario(rut_eliminar:str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute(
        """
        delete from usuarios where rut_user = :rut
        """, {"rut" :rut_eliminar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no Encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario Eliminado Correctamente"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
#Patch: Altualizar algunos datos noma
from typing import Optional
@router.patch("/{rut_actualizar}")
def actualizar_parcial(rut_actualizar:str, nombre_user:Optional[str]=None, p_apellido:Optional[str]=None, 
                       s_apellido:Optional[str]=None, correo_user:Optional[str]=None, 
                       contrasena_user:Optional[str]=None, id_genero:Optional[int]=None, id_rol:Optional[int]=None):
    try:
        if not nombre_user and not p_apellido and not s_apellido and not correo_user and not contrasena_user and not id_genero and not id_rol:
            raise HTTPException(status_code=400, detail="Debe enviar por lo menos 1 dato")
        
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"rut_user": rut_actualizar}

        if nombre_user:
            campos.append("nombre_user = :nombre_user")
            valores["nombre_user"] = nombre_user
        if p_apellido:
            campos.append("p_apellido = :p_apellido")
            valores["p_apellido"] = p_apellido
        if s_apellido:
            campos.append("s_apellido = :s_apellido")
            valores["s_apellido"] = s_apellido
        if correo_user:
            campos.append("correo_user = :correo_user")
            valores["correo_user"] = correo_user
        if contrasena_user:
            campos.append("contrasena_user = :contrasena_user")
            valores["contrasena_user"] = contrasena_user
        if id_genero:
            campos.append("id_genero = :id_genero")
            valores["id_genero"] = id_genero
        if id_rol:
            campos.append("id_rol = :id_rol")
            valores["id_rol"] = id_rol
        
        cursor.execute(f"update usuarios set {', '.join(campos)} where rut_user = :rut_user", valores)
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario actualizado correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
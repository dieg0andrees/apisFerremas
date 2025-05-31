from fastapi import APIRouter, HTTPException
from usuarios.database import get_conexion
from pydantic import BaseModel
from datetime import date

router = APIRouter(
    prefix="/producto_pedido",
    tags=["Producto Pedido"]
)


#Aca se podran ver todos los productos pedidos que se han hecho
@router.get('/')
def obtener_productos_pedidos():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT
            producto_pedido.ID_PEDIDO,
            producto.NOMBRE_PRODUCTO,
            marca.DESCRIPCION,
            producto.PRECIO_PRODUCTO,
            tipo_producto.DESCRIPCION as tp,
            producto_pedido.CANTIDAD_PRODUCTO,
            ESTADO_PEDIDO.DESCRIPCION,
            pedido.RUT_USER,
            usuarios.nombre_user,
            usuarios.P_APELLIDO
        FROM producto_pedido
        join producto on producto_pedido.ID_PRODUCTO = producto.ID_PRODUCTO
        join marca on producto.id_marca = marca.id_marca
        join tipo_producto on producto.ID_TIPO_PRODUCTO = tipo_producto.ID_TIPO_PRODUCTO
        join pedido on producto_pedido.ID_PEDIDO = pedido.ID_PEDIDO
        join estado_pedido on ESTADO_PEDIDO.ID_ESTADO_PEDIDO = PEDIDO.ID_ESTADO_PEDIDO
        join usuarios on pedido.RUT_USER = usuarios.RUT_USER
        """)
        producto_pedidos = []
        for id_pedido, nombre_producto, descripcion, precio_producto, tp, cantidad_producto, ep, rut, nombre_user, apellido in cursor:
            producto_pedidos.append({
                "id_pedido": id_pedido,
                "nombre_producto": nombre_producto,
                "marca_descripcion": descripcion,
                "precio_producto": precio_producto,
                "tipo_producto": tp,
                "cantidad_producto": cantidad_producto,
                "estado_pedido": ep,
                "rut": rut,
                "nombre_user": nombre_user,
                "apellido": apellido
            })
        cursor.close()
        cone.close()
        return producto_pedidos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
#y aca wn podras ver el producto_pedido pero por el id 

@router.get("/{id_pedido}")
def detalle_pedido(id_pedido: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT   
            producto.NOMBRE_PRODUCTO,
            marca.DESCRIPCION,
            producto.PRECIO_PRODUCTO,
            tipo_producto.DESCRIPCION as tp,
            producto_pedido.CANTIDAD_PRODUCTO,
            ESTADO_PEDIDO.DESCRIPCION,
            pedido.RUT_USER,
            usuarios.nombre_user,
            usuarios.P_APELLIDO
        FROM producto_pedido
        JOIN producto ON producto_pedido.ID_PRODUCTO = producto.ID_PRODUCTO
        JOIN marca ON producto.ID_MARCA = marca.ID_MARCA
        JOIN tipo_producto ON producto.ID_TIPO_PRODUCTO = tipo_producto.ID_TIPO_PRODUCTO
        join pedido on producto_pedido.ID_PEDIDO = pedido.ID_PEDIDO
        join estado_pedido on ESTADO_PEDIDO.ID_ESTADO_PEDIDO = PEDIDO.ID_ESTADO_PEDIDO
        join usuarios on pedido.RUT_USER = usuarios.RUT_USER
        where producto_pedido.id_pedido =: id_pedido                       
        """, {"id_pedido": id_pedido})

        detalles = cursor.fetchall()
        cursor.close()
        cone.close()

        if not detalles:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")

        productos = []
        for detalle in detalles:
            productos.append({
                "nombre_producto": detalle[0],
                "marca_descripcion": detalle[1],
                "precio_producto": detalle[2],
                "tipo_producto": detalle[3],
                "cantidad_producto": detalle[4],
                "estado_pedido": detalle[5],
                "rut_user": detalle[6],
                "nombre_user": detalle[7],
                "primer_apellido": detalle[8]
            })

        return {
            "id_pedido": id_pedido,
            "productos": productos
        }

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

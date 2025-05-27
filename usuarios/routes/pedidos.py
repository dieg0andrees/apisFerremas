from fastapi import APIRouter, HTTPException
from usuarios.database import get_conexion
from pydantic import BaseModel
from datetime import date

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

class PedidoCrear(BaseModel):
    fecha_pedido: date
    cantidad_pedido: int
    subtotal_pedido: int
    rut_user: str
    id_estado_pedido: int  # Nuevo campo
    id_productos: list[int]

@router.post("/")
def crear_pedido(pedido: PedidoCrear):
    cone = None
    cursor = None
    try:
        cone = get_conexion()
        cursor = cone.cursor()

        id_pedido_var = cursor.var(int)

        cursor.execute("""
            BEGIN
                INSERT INTO pedido (
                    id_pedido, fecha_pedido, cantidad_pedido, subtotal_pedido, rut_user, id_estado_pedido
                )
                VALUES (
                    seq_id_pedido.NEXTVAL, :fecha_pedido, :cantidad_pedido, :subtotal_pedido, :rut_user, :id_estado_pedido
                )
                RETURNING id_pedido INTO :id_pedido;
            END;
        """, {
            "fecha_pedido": pedido.fecha_pedido,
            "cantidad_pedido": pedido.cantidad_pedido,
            "subtotal_pedido": pedido.subtotal_pedido,
            "rut_user": pedido.rut_user,
            "id_estado_pedido": pedido.id_estado_pedido,
            "id_pedido": id_pedido_var
        })

        id_pedido = id_pedido_var.getvalue()

        if not pedido.id_productos:
            raise HTTPException(status_code=400, detail="La lista de productos no puede estar vacía.")

        for id_producto in pedido.id_productos:
            cursor.execute("""
                INSERT INTO producto_pedido (id_producto_pedido, id_producto, id_pedido)
                VALUES (seq_producto_pedido.NEXTVAL, :id_producto, :id_pedido)
            """, {
                "id_producto": id_producto,
                "id_pedido": id_pedido
            })

        cone.commit()

        return {
            "mensaje": "Pedido y productos asociados creados correctamente",
            "id_pedido": id_pedido,
            "productos": pedido.id_productos
        }

    except Exception as ex:
        if cone:
            cone.rollback()
        raise HTTPException(status_code=500, detail=str(ex))

    finally:
        if cursor:
            cursor.close()
        if cone:
            cone.close()

@router.get("/")
def obtener_pedidos():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT
            pedido.ID_PEDIDO,
            pedido.FECHA_PEDIDO,
            pedido.CANTIDAD_PEDIDO,
            pedido.SUBTOTAL_PEDIDO,
            pedido.RUT_USER,
            estado_pedido.DESCRIPCION
        FROM pedido
        join estado_pedido on pedido.id_estado_pedido = estado_pedido.ID_ESTADO_PEDIDO
        """)
        pedidos = []

        for id_pedido, fecha_pedido, cantidad_pedido, subtotal_pedido, rut_user, descripcion in cursor:
            pedidos.append({
                "id_pedido": id_pedido,
                "fecha_pedido": fecha_pedido,
                "cantidad_pedido": cantidad_pedido,
                "subtotal_pedido": subtotal_pedido,
                "rut_user": rut_user,
                "descripcion": descripcion
            })
        cursor.close()
        cone.close()
        return pedidos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

@router.get("/")
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
            tipo_producto.DESCRIPCION as tp
        FROM producto_pedido
        join producto on producto_pedido.ID_PRODUCTO = producto.ID_PRODUCTO
        join marca on producto.id_marca = marca.id_marca
        join tipo_producto on producto.ID_TIPO_PRODUCTO = tipo_producto.ID_TIPO_PRODUCTO
        """)
        producto_pedidos = []
        for id_pedido, nombre_producto, descripcion, precio_producto, tp in cursor:
            producto_pedidos.append({
                "id_pedido": id_pedido,
                "nombre_producto": nombre_producto,
                "marca_descripcion": descripcion,
                "precio_producto": precio_producto,
                "tipo_producto": tp
            })
        cursor.close()
        cone.close()
        return producto_pedidos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
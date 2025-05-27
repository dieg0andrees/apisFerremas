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


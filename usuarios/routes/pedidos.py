from fastapi import APIRouter, HTTPException
from usuarios.database import get_conexion
from pydantic import BaseModel
from datetime import date

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

class ProductoPedido(BaseModel):
    id_producto: int
    cantidad_producto: int

class PedidoCrear(BaseModel):
    fecha_pedido: date
    cantidad_pedido: int
    subtotal_pedido: int
    rut_user: str
    id_estado_pedido: int
    id_productos: list[ProductoPedido]

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

        for producto in pedido.id_productos:
            cursor.execute("""
                INSERT INTO producto_pedido (id_producto_pedido, id_producto, id_pedido, cantidad_producto)
                VALUES (seq_producto_pedido.NEXTVAL, :id_producto, :id_pedido, :cantidad_producto)
            """, {
                "id_producto": producto.id_producto,
                "id_pedido": id_pedido,
                "cantidad_producto": producto.cantidad_producto
            })

        cone.commit()

        return {
            "mensaje": "Pedido creados correctamente",
            "id_pedido": id_pedido,
            "productos": [{"id": p.id_producto, "cantidad": p.cantidad_producto} for p in pedido.id_productos]
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
    
    
@router.get("/{id_pedido}")
def buscar_pedido(id_pedido: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT
            pedido.FECHA_PEDIDO,
            pedido.CANTIDAD_PEDIDO,
            pedido.SUBTOTAL_PEDIDO,
            pedido.RUT_USER,
            estado_pedido.DESCRIPCION
        FROM pedido
        join estado_pedido on pedido.id_estado_pedido = estado_pedido.ID_ESTADO_PEDIDO
        where id_pedido =: id_pedido """, 
        {"id_pedido": id_pedido})

        pedido = cursor.fetchone()
        cursor.close()
        cone.close()

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no Encontrado")
        return{
            "id_pedido": id_pedido,
            "fecha_pedido": pedido[0],
            "cantidad_pedido": pedido[1],
            "subtotal_pedido": pedido[2],
            "rut_user": pedido[3],
            "estado_pedido": pedido[4],
        }        
  
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

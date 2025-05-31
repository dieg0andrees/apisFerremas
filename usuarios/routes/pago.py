from fastapi import APIRouter, HTTPException
from usuarios.database import get_conexion
from pydantic import BaseModel
from datetime import date
router = APIRouter(
    prefix="/pago",
    tags= ["Pago"]
)

@router.get('/')
def obtener_pagos():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT
            PAGO.ID_PAGO,
            PAGO.FECHA_PAGO,
            PAGO.MONTO_PAGAR,
            PAGO.URL_COMPROBANTE,
            MEDIO_PAGO.DESCRIPCION,
            ESTADO_PAGO.DESCRIPCION,
            PAGO.ID_PEDIDO
        FROM PAGO
        JOIN MEDIO_PAGO ON PAGO.ID_MEDIO_PAGO = MEDIO_PAGO.ID_MEDIO_PAGO
        JOIN ESTADO_PAGO ON PAGO.ID_ESTADO_PAGO = ESTADO_PAGO.ID_ESTADO_PAGO
        """)
        pago = []

        for id_pago, fecha_pago, monto_pagar, url_comprobante, mp, ep, id_pedido in cursor:
            pago.append({
                "id_pago": id_pago,
                "fecha_pago": fecha_pago,
                "monto_pagar": monto_pagar,
                "url_comprobante": url_comprobante,
                "medio_pago": mp,
                "estado_pago": ep,
                "id_pedido": id_pedido
            })
        cursor.close()
        cone.close()
        return pago
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

from typing import Optional


class PagoActualizar(BaseModel):
    fecha_pago: Optional[str] = None
    monto_pagar: Optional[float] = None
    url_comprobante: Optional[str] = None
    id_medio_pago: Optional[int] = None
    id_estado_pago: Optional[int] = None
    id_pedido: Optional[int] = None


@router.patch("/{id_pago}")
def actualizar_pago(id_pago: int, datos: PagoActualizar):
    try:
        campos = []
        valores = {"id_pago": id_pago}

        if datos.fecha_pago is not None:
            campos.append("FECHA_PAGO = :fecha_pago")
            valores["fecha_pago"] = datos.fecha_pago
        if datos.monto_pagar is not None:
            campos.append("MONTO_PAGAR = :monto_pagar")
            valores["monto_pagar"] = datos.monto_pagar
        if datos.url_comprobante is not None:
            campos.append("URL_COMPROBANTE = :url_comprobante")
            valores["url_comprobante"] = datos.url_comprobante
        if datos.id_medio_pago is not None:
            campos.append("ID_MEDIO_PAGO = :id_medio_pago")
            valores["id_medio_pago"] = datos.id_medio_pago
        if datos.id_estado_pago is not None:
            campos.append("ID_ESTADO_PAGO = :id_estado_pago")
            valores["id_estado_pago"] = datos.id_estado_pago
        if datos.id_pedido is not None:
            campos.append("ID_PEDIDO = :id_pedido")
            valores["id_pedido"] = datos.id_pedido

        if not campos:
            raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")

        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute(f"""
            UPDATE PAGO
            SET {', '.join(campos)}
            WHERE ID_PAGO = :id_pago
        """, valores)

        if cursor.rowcount == 0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        cone.commit()
        cursor.close()
        cone.close()

        return {"mensaje": "Pago actualizado correctamente"}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/{id_pago}")
def buscar_pago(id_pago: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
        SELECT
            PAGO.FECHA_PAGO,
            PAGO.MONTO_PAGAR,
            PAGO.URL_COMPROBANTE,
            MEDIO_PAGO.DESCRIPCION,
            ESTADO_PAGO.DESCRIPCION,
            PAGO.ID_PEDIDO
        FROM PAGO
        JOIN MEDIO_PAGO ON PAGO.ID_MEDIO_PAGO = MEDIO_PAGO.ID_MEDIO_PAGO
        JOIN ESTADO_PAGO ON PAGO.ID_ESTADO_PAGO = ESTADO_PAGO.ID_ESTADO_PAGO
        where id_pago =: id_pago
        """, {"id_pago": id_pago})
        
        pago = cursor.fetchone()
        cursor.close()
        cone.close()
        if not pago:
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        return{
            "id_pago": id_pago,
            "fecha_pago": pago[0],
            "monto_pagar": pago[1],
            "url_comprobante": pago[2],
            "medio_pago": pago[3],
            "estado_pago": pago[4],
            "id_pedido": pago[5]
        }
    except Exception as ex:
        raise HTTPException (status_code=500, detail=str(ex))



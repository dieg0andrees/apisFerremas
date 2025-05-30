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

@router.patch("/{id_pago}")
def actualizar_pago_parcial(id_pago: int, fecha_pago: Optional[str] = None, monto_pagar: Optional[float] = None,
                            url_comprobante: Optional[str] = None, id_medio_pago: Optional[int] = None,
                            id_estado_pago: Optional[int] = None, id_pedido: Optional[int] = None):
    try:
        if not any([fecha_pago, monto_pagar, url_comprobante, id_medio_pago, id_estado_pago, id_pedido]):
            raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")

        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"id_pago": id_pago}

        if fecha_pago:
            campos.append("FECHA_PAGO = :fecha_pago")
            valores["fecha_pago"] = fecha_pago
        if monto_pagar:
            campos.append("MONTO_PAGAR = :monto_pagar")
            valores["monto_pagar"] = monto_pagar
        if url_comprobante:
            campos.append("URL_COMPROBANTE = :url_comprobante")
            valores["url_comprobante"] = url_comprobante
        if id_medio_pago:
            campos.append("ID_MEDIO_PAGO = :id_medio_pago")
            valores["id_medio_pago"] = id_medio_pago
        if id_estado_pago:
            campos.append("ID_ESTADO_PAGO = :id_estado_pago")
            valores["id_estado_pago"] = id_estado_pago
        if id_pedido:
            campos.append("ID_PEDIDO = :id_pedido")
            valores["id_pedido"] = id_pedido

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




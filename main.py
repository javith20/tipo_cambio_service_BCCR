from fastapi import FastAPI, Request, Depends, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
from tipo_cambio import obtener_tipo_cambio
from db import SessionLocal, TipoCambio, ConsultaLog, init_db
import os
from fastapi import Query
app = FastAPI()
init_db()

API_KEY = os.getenv("API_KEY")

class ConversionRequest(BaseModel):
    monto: float
    fecha: str
    tipo: str  # "compra" o "venta"
    sentido: str  # "crc_usd" o "usd_crc"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/convertir/")
async def convertir(
    datos: ConversionRequest,
    request: Request,
    x_api_key: str = Header(None),
    db=Depends(get_db)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")

    monto = datos.monto
    fecha = datos.fecha
    tipo = datos.tipo
    sentido = datos.sentido

    # Buscar en la base de datos primero
    tipo_cambio = db.query(TipoCambio).filter_by(fecha=fecha, tipo=tipo).first()
    if not tipo_cambio:
        valor = obtener_tipo_cambio(datetime.strptime(fecha, "%Y-%m-%d"), tipo)
        tipo_cambio = TipoCambio(fecha=fecha, tipo=tipo, valor=valor)
        db.add(tipo_cambio)
        db.commit()

    if sentido == "crc_usd":
        monto_colones = monto
        monto_usd = monto_colones / tipo_cambio.valor
    elif sentido == "usd_crc":
        monto_usd = monto
        monto_colones = monto_usd * tipo_cambio.valor
    else:
        raise HTTPException(status_code=400, detail="Sentido inválido. Use 'crc_usd' o 'usd_crc'.")

    log = ConsultaLog(
        fecha=datetime.now(),
        ip=request.client.host,
        api_token=x_api_key,
        monto_colones=monto_colones,
        tipo=tipo,
        fecha_cambio=fecha,
        resultado_usd=monto_usd
    )
    db.add(log)
    db.commit()

    return {
        "fecha": fecha,
        "tipo": tipo,
        "tipo_cambio": tipo_cambio.valor,
        "sentido": sentido,
        "monto_colones": monto_colones,
        "monto_usd": monto_usd
    }
@app.get("/tipo_cambio/")
async def obtener_tipo_cambio_fecha(
    fecha: str = Query(..., description="Fecha en formato YYYY-MM-DD"),
    db=Depends(get_db)
):
    compra = db.query(TipoCambio).filter_by(fecha=fecha, tipo="compra").first()
    venta = db.query(TipoCambio).filter_by(fecha=fecha, tipo="venta").first()

    # Si no existe en la base, consulta al BCCR y guarda
    if not compra:
        valor_compra = obtener_tipo_cambio(datetime.strptime(fecha, "%Y-%m-%d"), "compra")
        compra = TipoCambio(fecha=fecha, tipo="compra", valor=valor_compra)
        db.add(compra)
        db.commit()
    if not venta:
        valor_venta = obtener_tipo_cambio(datetime.strptime(fecha, "%Y-%m-%d"), "venta")
        venta = TipoCambio(fecha=fecha, tipo="venta", valor=valor_venta)
        db.add(venta)
        db.commit()

    return {
        "fecha": fecha,
        "venta": venta.valor,
        "compra": compra.valor
    }
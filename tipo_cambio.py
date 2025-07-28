import os
from datetime import datetime
from zeep import Client
from dotenv import load_dotenv

load_dotenv()

WSDL_URL = "https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx?WSDL"

def obtener_tipo_cambio(fecha: datetime, tipo: str) -> float:
    # tipo: "compra" o "venta"
    indicador = os.getenv("BCCR_INDICADOR_COMPRA") if tipo == "compra" else os.getenv("BCCR_INDICADOR_VENTA")
    client = Client(wsdl=WSDL_URL)
    params = {
        "Indicador": indicador,
        "FechaInicio": fecha.strftime("%d/%m/%Y"),
        "FechaFinal": fecha.strftime("%d/%m/%Y"),
        "Nombre": os.getenv("BCCR_NOMBRE"),
        "SubNiveles": os.getenv("BCCR_SUBNIVELES"),
        "CorreoElectronico": os.getenv("BCCR_CORREO"),
        "Token": os.getenv("BCCR_TOKEN")
    }
    response = client.service.ObtenerIndicadoresEconomicos(**params)
    series = response["_value_1"]["_value_1"]
    for item in series:
        datos = item["INGC011_CAT_INDICADORECONOMIC"]
        fecha_resultado = datos["DES_FECHA"].date()
        if fecha_resultado == fecha.date():
            return float(datos["NUM_VALOR"])
    raise ValueError(f"No se encontró tipo de cambio para la fecha {fecha.strftime('%Y-%m-%d')}")
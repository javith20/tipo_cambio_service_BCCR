from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tipo_cambio.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TipoCambio(Base):
    __tablename__ = "tipos_cambio"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, index=True)
    tipo = Column(String, index=True)  # compra o venta
    valor = Column(Float)

class ConsultaLog(Base):
    __tablename__ = "consultas_log"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now)
    ip = Column(String)
    api_token = Column(String)
    monto_colones = Column(Float)
    tipo = Column(String)
    fecha_cambio = Column(String)
    resultado_usd = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)
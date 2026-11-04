from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI(
    title="Resoft Control API",
    description="API interna para monitoreo y alertas del equipo.",
    version="1.0.0"
)

# Estructura de los datos que entran (lo validamos con Pydantic, un lujo)
class AlertaServidor(BaseModel):
    servicio: str
    estado: str  # ej: "OK", "WARNING", "CRITICAL"
    detalle: Optional[str] = None
    responsable: str

# Una listita en memoria simulando una base de datos para arrancar
historial_alertas: List[dict] = []

@app.get("/")
def home():
    return {"mensaje": "¡Servidor de Resoft andando a pleno!", "status": "online"}

@app.post("/api/alertas/")
def registrar_alerta(alerta: AlertaServidor):
    """Registra una nueva alerta o estado de un servicio del sistema."""
    registro = {
        "servicio": alerta.servicio,
        "estado": alerta.estado.upper(),
        "detalle": alerta.detalle,
        "responsable": alerta.responsable,
        "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    historial_alertas.append(registro)
    return {"mensaje": "Alerta registrada con éxito, pa.", "data": registro}

@app.get("/api/alertas/", response_model=List[dict])
def ver_alertas():
    """Devuelve todo el historial de alertas registradas."""
    return historial_alertas


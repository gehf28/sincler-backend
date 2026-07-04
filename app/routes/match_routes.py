# backend/app/api/v1/endpoints/match_routes.py

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import StreamingResponse
from app.models.match import MatchRequest
from datetime import datetime, timedelta

# 🚀 1. CORRECCIÓN: Importa ambos servicios correctamente
from app.services.analysis.freemium_service import analyze_freemium_stream
from app.services.analysis.mundial_service import analyze_mundial_stream  # <-- ¡Faltaba este!
from app.services.database.history_service import obtener_ultimas_consultas

router = APIRouter()

cooldown_store = {}

def verificar_limite_tiempo(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host

    now = datetime.now()
    
    if client_ip in cooldown_store:
        last_request_time = cooldown_store[client_ip]
        time_passed = now - last_request_time
        
        if time_passed < timedelta(minutes=15):
            time_remaining = timedelta(minutes=15) - time_passed
            minutes = int(time_remaining.total_seconds() // 60)
            seconds = int(time_remaining.total_seconds() % 60)
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Límite freemium alcanzado. Espera {minutes}m {seconds}s."
            )
            
    cooldown_store[client_ip] = now


# =========================================================================
# 🌍 1. MÓDULO: COPA MUNDIAL 2026 (CORREGIDO)
# =========================================================================
@router.post("/api/analyze/mundial")
async def analyze_match_mundial(data: MatchRequest, request: Request):
    verificar_limite_tiempo(request)
    
    # 🚀 REPARADO: Ahora sí llama al flujo que usa el WORLD_CUP_PROMPT
    return StreamingResponse(
        analyze_mundial_stream(data.team1, data.team2, data.league, data.date),
        media_type="text/event-stream"
    )


# =========================================================================
# ⚽ 2. MÓDULO: PARTIDOS EN GENERAL (LIGAS Y CLUBES)
# =========================================================================
@router.post("/api/analyze/general")
async def analyze_match_general(data: MatchRequest, request: Request):
    verificar_limite_tiempo(request)
    
    # Mantiene el servicio estándar para el análisis clásico de clubes
    return StreamingResponse(
        analyze_freemium_stream(data.team1, data.team2, data.league, data.date),
        media_type="text/event-stream"
    )
    
@router.get("/api/historial")
async def get_historial(tipo: str = "general"):
    """Endpoint que consume el frontend para listar los análisis recientes"""
    return obtener_ultimas_consultas(tipo_analisis=tipo, limite=10)

# ... al final de tu match_routes.py

@router.post("/api/registro")
async def registro_endpoint(request: Request):
    data = await request.json()
    from app.services.database.registro_service import registrar_evento_o_lead
    
    registrar_evento_o_lead(
        tipo=data.get("tipo"),
        seccion=data.get("seccion"),
        nombre=data.get("nombre"),
        correo=data.get("correo")
    )
    return {"status": "ok"}
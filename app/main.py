from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Importamos los modelos y servicios necesarios
from app.models.match import MatchRequest
from app.services.analysis.mundial_service import analyze_mundial_stream

# Importamos las rutas estándar de tu aplicación
from app.routes.match_routes import router as match_router

import os
import uvicorn

app = FastAPI(
    title="Sincler IA API",
    description="Motor de análisis predictivo deportivo en tiempo real",
    version="1.0.0"
)

# # 🌐 CONFIGURACIÓN DE CORS (Crucial para conectar con Next.js)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], # En producción con Seenode, puedes cambiar esto por la URL de tu frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛣️ ENRUTADORES DE MÓDULOS ESTÁNDAR
# Este incluye el endpoint "/api/analyze" para el Análisis General (Clubs y Ligas)
app.include_router(match_router)


# 🏠 RUTA DE VERIFICACIÓN
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Sincler IA Engine funcionando correctamente"
    }


# 🏆 ENDPOINT EXCLUSIVO: MÓDULO MUNDIAL 2026
# Escucha directamente en /api/analyze/mundial y ejecuta el prompt especializado
# @app.post("/api/analyze/mundial")
# async def analyze_mundial_match(data: MatchRequest):
#     return StreamingResponse(
#         analyze_mundial_stream(data.team1, data.team2, data.league, data.date),
#         media_type="text/event-stream"
#     )

if __name__ == "__main__":
    # Seenode asignará un puerto automáticamente en la variable de entorno PORT
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
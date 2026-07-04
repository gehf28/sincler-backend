# # backend/app/services/database/history_service.py

# import os
# import json
# from datetime import datetime
# from sqlalchemy import create_engine, text

# # Cargamos la URL de la base de datos
# DATABASE_URL = os.getenv("DATABASE_URL")

# # Motor clásico y robusto
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# def guardar_en_historial(team1: str, team2: str, resultado_json: dict):
#     """Guarda el resultado final del análisis en la tabla del mundial"""
#     try:
#         with engine.connect() as conn:
#             query = text("""
#                 INSERT INTO historial_consultas_mundial (team1, team2, resultado_json)
#                 VALUES (:team1, :team2, :resultado_json);
#             """)
#             # Convertimos el dict a un string JSON compatible con PostgreSQL
#             json_str = json.dumps(resultado_json)
            
#             conn.execute(query, {"team1": team1, "team2": team2, "resultado_json": json_str})
#             conn.commit()
#             print(f"✅ [Supabase - Postgres] Guardado con éxito: {team1} vs {team2}")
#     except Exception as e:
#         print(f"❌ Error al guardar en historial_consultas_mundial: {e}")

# def obtener_ultimas_consultas():
#     """Trae los últimos 10 análisis del mundial para mostrarlos en el frontend"""
#     try:
#         with engine.connect() as conn:
#             query = text("""
#                 SELECT id, team1, team2, resultado_json, fecha_consulta 
#                 FROM historial_consultas_mundial 
#                 ORDER BY fecha_consulta DESC 
#                 LIMIT 10;
#             """)
#             result = conn.execute(query)
#             rows = result.fetchall()
            
#             historial = []
#             for row in rows:
#                 # Dependiendo de la versión de Supabase/Postgres, resultado_json puede venir como dict o como string
#                 res_json = row[3]
#                 if isinstance(res_json, str):
#                     res_json = json.loads(res_json)
                
#                 # Manejo seguro de la fecha
#                 fecha = row[4].isoformat() if isinstance(row[4], datetime) else str(row[4]) if row[4] else None

#                 historial.append({
#                     "id": row[0],
#                     "team1": row[1],
#                     "team2": row[2],
#                     "resultado_json": res_json,
#                     "fecha_consulta": fecha
#                 })
                
#             return historial
#     except Exception as e:
#         print(f"❌ Error al obtener el historial de Supabase: {e}")
#         return []

# backend/app/services/database/history_service.py

import os
import json
from datetime import datetime
from sqlalchemy import create_engine, text

# Cargamos la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor clásico y robusto
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def guardar_en_historial(team1: str, team2: str, resultado_json: dict, tipo_analisis: str = "general"):
    """
    Guarda el resultado en la tabla unificada especificando si es 'general' o 'mundial'.
    """
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO historial_consultas (team1, team2, resultado_json, tipo_analisis)
                VALUES (:team1, :team2, :resultado_json, :tipo_analisis);
            """)
            # Convertimos el dict a un string JSON compatible con PostgreSQL
            json_str = json.dumps(resultado_json)
            
            conn.execute(query, {
                "team1": team1, 
                "team2": team2, 
                "resultado_json": json_str,
                "tipo_analisis": tipo_analisis
            })
            conn.commit()
            print(f"✅ [Supabase - Postgres] Guardado con éxito ({tipo_analisis}): {team1} vs {team2}")
    except Exception as e:
        print(f"❌ Error al guardar en historial_consultas ({tipo_analisis}): {e}")

def obtener_ultimas_consultas(tipo_analisis: str = "general", limite: int = 10):
    """
    Trae los últimos análisis filtrando estrictamente por el tipo ('general' o 'mundial').
    """
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT id, team1, team2, resultado_json, fecha_consulta 
                FROM historial_consultas 
                WHERE tipo_analisis = :tipo_analisis
                ORDER BY fecha_consulta DESC 
                LIMIT :limite;
            """)
            result = conn.execute(query, {"tipo_analisis": tipo_analisis, "limite": limite})
            rows = result.fetchall()
            
            historial = []
            for row in rows:
                res_json = row[3]
                if isinstance(res_json, str):
                    res_json = json.loads(res_json)
                
                # Manejo seguro de la fecha
                fecha = row[4].isoformat() if isinstance(row[4], datetime) else str(row[4]) if row[4] else None

                historial.append({
                    "id": row[0],
                    "team1": row[1],
                    "team2": row[2],
                    "resultado_json": res_json,
                    "fecha_consulta": fecha
                })
                
            return historial
    except Exception as e:
        print(f"❌ Error al obtener el historial ({tipo_analisis}) de Supabase: {e}")
        return []
# # backend/app/services/analysis/mundial_service.py

# import json
# import os
# from openai import AsyncOpenAI
# # Importamos las herramientas de búsqueda y contexto compartidas
# from app.services.tavily.tavily_service import search_match_data
# from app.services.openai.context_builder import build_match_context
# # Importamos tu nuevo prompt exclusivo para el mundial
# from app.services.prompts.mundial_prompt import WORLD_CUP_PROMPT 

# # Inicializamos el cliente de OpenAI usando la API Key del entorno
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# async def analyze_mundial_stream(team1, team2, league="Copa Mundial 2026", match_date=""):
#     try:
#         # 1. Buscamos datos frescos en Tavily sobre las selecciones (lesiones, alineaciones, noticias de última hora)
#         tavily_data = search_match_data(team1, team2, league, match_date)
#         context = build_match_context(tavily_data)
        
#         # 2. Generamos el prompt inyectándole el contexto extraído de Tavily
#         # Usamos .format pasando las variables necesarias
#         prompt = WORLD_CUP_PROMPT.format(
#             context=context,
#             team1=team1,
#             team2=team2
#         )

#         # 3. Forzamos el streaming de OpenAI con el json_object activado
#         response = await client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             response_format={"type": "json_object"}, # Evita que rompa el flujo estructurado
#             temperature=0.3,
#             stream=True
#         )
        
#         # 4. Emitimos cada fragmento (token) en tiempo real character-by-character
#         async for chunk in response:
#             content = chunk.choices[0].delta.content
#             if content:
#                 yield content

#     except Exception as e:
#         print(f"Error en streaming Mundial: {str(e)}")
#         # Si algo falla en la llamada, emitimos un JSON controlado idéntico al esquema esperado
#         yield json.dumps({
#             "team1": team1,
#             "team2": team2,
#             "favorito": team1,
#             "riesgo": "Medio",
#             "comentario_general": "El motor táctico experimentó un inconveniente temporal al recopilar las variables de Tavily o el Stream de OpenAI.",
#             "probabilidades": {"local": 34, "empate": 33, "visita": 33},
#             "lineaCorners": "Evaluación no disponible",
#             "jugadorGoleadorProbable": "No determinado",
#             "quienClasifica": "No determinado"
#         })

# backend/app/services/analysis/mundial_service.py

import json
import os
from openai import AsyncOpenAI
from app.services.tavily.tavily_service import search_match_data
from app.services.openai.context_builder import build_match_context
from app.services.prompts.mundial_prompt import WORLD_CUP_PROMPT 

# 🚀 IMPORTACIÓN SEGURA: Desde el nuevo archivo independiente para evitar bucles
from app.services.database.history_service import guardar_en_historial

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def analyze_mundial_stream(team1, team2, league="Copa Mundial 2026", match_date=""):
    try:
        tavily_data = search_match_data(team1, team2, league, match_date)
        context = build_match_context(tavily_data)
        
        prompt = WORLD_CUP_PROMPT.format(
            context=context,
            team1=team1,
            team2=team2
        )

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}, 
            temperature=0.3,
            stream=True
        )
        
        # Variable local para ir guardando una copia del JSON completo
        texto_acumulado = ""

        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                texto_acumulado += content  # Acumulamos el token
                yield content  # Lo enviamos en tiempo real al cliente

        # 🚀 Al terminar el streaming de OpenAI, guardamos el resultado
        try:
            json_final = json.loads(texto_acumulado.strip())
            guardar_en_historial(team1, team2, json_final, tipo_analisis="mundial")
        except Exception as json_err:
            print(f"❌ Error al parsear el JSON final acumulado: {str(json_err)}")

    except Exception as e:
        print(f"Error en streaming Mundial: {str(e)}")
        yield json.dumps({
            "team1": team1,
            "team2": team2,
            "favorito": team1,
            "riesgo": "Medio",
            "comentario_general": "El motor táctico experimentó un inconveniente temporal.",
            "probabilidades": {"local": 34, "empate": 33, "visita": 33},
            "lineaCorners": "Evaluación no disponible",
            "jugadorGoleadorProbable": "No determinado",
            "quienClasifica": "No determinado"
        })
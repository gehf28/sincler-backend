# import json
# from openai import AsyncOpenAI
# from app.services.tavily.tavily_service import search_match_data
# from app.services.openai.context_builder import build_match_context
# from app.services.prompts.freemium_prompt import build_freemium_prompt # Asegúrate de tener tu generador de prompt estructurado

# client = AsyncOpenAI()

# async def analyze_freemium_stream(team1, team2, league="", match_date=""):
#     try:
#         # 1. Buscamos datos en Tavily de la misma forma estructurada
#         tavily_data = search_match_data(team1, team2, league, match_date)
#         context = build_match_context(tavily_data)
        
#         # 2. Generamos el prompt estructurado para la IA
#         prompt = build_freemium_prompt(context, team1, team2)

#         # 3. Forzamos el streaming de OpenAI garantizando salida de tipo objeto JSON
#         response = await client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             response_format={"type": "json_object"},
#             stream=True
#         )
        
#         # 4. Emitimos cada fragmento (token) en tiempo real
#         async for chunk in response:
#             content = chunk.choices[0].delta.content
#             if content:
#                 yield content

#     except Exception as e:
#         print(f"Error en streaming Freemium: {str(e)}")
#         yield json.dumps({
#             "team1": team1,
#             "team2": team2,
#             "comentario_general": "Hubo un inconveniente técnico al transmitir los datos."
#         })

# backend/app/services/analysis/freemium_service.py

import json
from openai import AsyncOpenAI
from app.services.tavily.tavily_service import search_match_data
from app.services.openai.context_builder import build_match_context
from app.services.prompts.freemium_prompt import build_freemium_prompt

# 🚀 IMPORTACIÓN DEL SERVICIO DE HISTORIAL
from app.services.database.history_service import guardar_en_historial

client = AsyncOpenAI()

async def analyze_freemium_stream(team1, team2, league="", match_date=""):
    try:
        tavily_data = search_match_data(team1, team2, league, match_date)
        context = build_match_context(tavily_data)
        
        prompt = build_freemium_prompt(context, team1, team2)

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            stream=True
        )
        
        # Variable local para ir guardando una copia del JSON completo
        texto_acumulado = ""

        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                texto_acumulado += content  # Acumulamos el token
                yield content

        # 🚀 Al terminar el streaming de OpenAI, guardamos el resultado como "general"
        try:
            json_final = json.loads(texto_acumulado.strip())
            guardar_en_historial(team1, team2, json_final, tipo_analisis="general")
        except Exception as json_err:
            print(f"❌ Error al parsear el JSON final acumulado en General: {str(json_err)}")

    except Exception as e:
        print(f"Error en streaming Freemium: {str(e)}")
        yield json.dumps({
            "team1": team1,
            "team2": team2,
            "comentario_general": "Hubo un inconveniente técnico al transmitir los datos."
        })
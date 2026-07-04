def build_premium_prompt(context, team1, team2):

    return f"""
Eres un analista profesional especializado en apuestas deportivas.

CONTEXTO:

{context}

Partido:
{team1} vs {team2}

Devuelve únicamente JSON.

{{
  "favorito":"",
  "probabilidadFavorito":0,
  "probabilidadEmpate":0,
  "probabilidadVisitante":0,
  "golesEsperadosLocal":0,
  "golesEsperadosVisitante":0,
  "over25":true,
  "ambosAnotan":true,
  "cornersEsperados":0,
  "tarjetasEsperadas":0,
  "riesgo":"Medio",
  "lesionesImportantes":[],
  "factoresClave":[],
  "escenarioEsperado":"",
  "marcadorProbable":"",
  "recomendacionApuesta":"",
  "comentario":""
}}
"""
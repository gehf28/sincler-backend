from tavily import TavilyClient
from app.core.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


# def build_tavily_query(team1: str, team2: str, league: str = "", match_date: str = ""):

#     parts = [
#         f"Partido de fútbol: {team1} vs {team2}"
#     ]

#     if league:
#         parts.append(f"Competencia: {league}")

#     if match_date:
#         parts.append(f"Fecha: {match_date}")

#     parts.append("""
# Buscar información actualizada:

# - lesiones
# - suspensiones
# - alineaciones probables
# - enfrentamientos directos 
# - últimos 5 partidos
# - estadísticas ofensivas y defensivas
# - tabla de posiciones
# - temporada actual
# - noticias recientes
# - Sofascore, Flashcore, WhoScored, ESPN
# - importancia del encuentro
# """)

#     return "\n".join(parts)


# def search_match_data(team1: str, team2: str, league: str = "", match_date: str = ""):

#     query = build_tavily_query(team1, team2, league, match_date)

#     response = client.search(
#         query=query,
#         search_depth="advanced",
#         max_results=2
#     )

#     return response

def build_tavily_query(team1: str, team2: str, league: str = "", match_date: str = "") -> str:
    
    parts = [f"{team1} vs {team2}"]
    
    if league:
        parts.append(league)
    if match_date:
        parts.append(match_date)
    
    parts.append("lesiones bajas suspensiones alineación probable forma reciente estadísticas head to head ranking fifa")
    
    return " ".join(parts)


def search_match_data(team1: str, team2: str, league: str = "", match_date: str = "") -> dict:
    
    query = build_tavily_query(team1, team2, league, match_date)
    
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=8,        # 5 es el punto justo: variedad sin desperdiciar tokens
        include_answer=True,  # Resumen corto generado por Tavily, ahorra tokens a OpenAI
    )
    
    # Devuelve solo lo útil, recorta el contenido largo
    return {
        "answer": response.get("answer"),
        "sources": [
            {
                "title": r["title"],
                "url": r["url"],
                "content": r["content"][:1000],  # limita caracteres por fuente
            }
            for r in response.get("results", [])
        ]
    }
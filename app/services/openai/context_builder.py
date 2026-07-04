def build_match_context(tavily_data: dict) -> str:

    context = f"""
RESUMEN GENERAL:
{tavily_data.get("answer", "")}

"""

    for source in tavily_data.get("sources", [])[:3]:

        context += f"""

FUENTE:
{source["title"]}

CONTENIDO:
{source["content"]}

"""

    return context
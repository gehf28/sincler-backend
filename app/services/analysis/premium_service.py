from app.services.tavily.tavily_service import search_match_data
from app.services.openai.context_builder import build_match_context
from app.services.openai.openai_service import ask_openai

from app.services.prompts.premium_prompt import (
    build_premium_prompt
)


def analyze_premium(team1, team2, league="", date=""):

    tavily_data = search_match_data(
        team1,
        team2,
        league,
        date
    )

    context = build_match_context(tavily_data)

    prompt = build_premium_prompt(
        context,
        team1,
        team2
    )

    return ask_openai(prompt)
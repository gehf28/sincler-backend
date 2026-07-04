from fastapi import APIRouter

from app.models.match import MatchRequest

from app.services.analysis.premium_service import (
    analyze_premium
)

router = APIRouter()


@router.post("/analyze-premium")
async def analyze_match_premium(data: MatchRequest):

    return analyze_premium(
        data.team1,
        data.team2,
        data.league,
        data.date
    )
from pydantic import BaseModel
from typing import Optional

class MatchRequest(BaseModel):
    team1: str
    team2: str
    league: Optional[str] = None
    date: Optional[str] = None
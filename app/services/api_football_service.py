import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"


def get_team_info(team_name: str):

    url = f"{BASE_URL}/teams"

    response = requests.get(
        url,
        headers=HEADERS,
        params={"search": team_name}
    )

    data = response.json()

    if not data.get("response"):
        return None

    team = data["response"][0]["team"]

    return {
        "id": team["id"],
        "name": team["name"],
        "logo": team["logo"]
    }
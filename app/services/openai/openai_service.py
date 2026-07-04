from openai import OpenAI
from app.core.config import OPENAI_API_KEY

# Mantenemos el cliente estándar compatible con llamadas estructuradas
client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_analysis(team1, team2, context):
    from app.services.prompts.freemium_prompt import build_freemium_prompt
    
    # Construimos el prompt usando tu plantilla estructurada
    prompt = build_freemium_prompt(context, team1, team2)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Responde únicamente JSON válido según la estructura solicitada por el usuario sin texto envolvente."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
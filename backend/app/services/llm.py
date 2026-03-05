import os
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

DIFFICULTY_PROMPTS = {
    "easier": """You are a music arranger. Simplify the given MusicXML score to make it easier to play:
- Remove ornaments (trills, mordents, turns)
- Simplify rhythms (replace 16th notes or smaller with 8th notes where possible)
- Keep the melody intact
Return ONLY the modified MusicXML. No explanation.""",
    "harder": """You are a music arranger. Make the given MusicXML score more challenging:
- Add appropriate ornaments
- Enrich rhythms with subdivisions
- Keep the original melody intact
Return ONLY the modified MusicXML. No explanation.""",
}


async def transform(musicxml_content: str, difficulty: str = "easier") -> str:
    prompt = DIFFICULTY_PROMPTS.get(difficulty, DIFFICULTY_PROMPTS["easier"])

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{prompt}\n\n{musicxml_content}",
    )

    return response.text

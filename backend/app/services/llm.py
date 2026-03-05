import os
import re
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

MODEL = "gemini-2.5-flash"


def _call(prompt: str) -> str:
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()


STEP1_PROMPT = """Extract all notes from this MusicXML as a JSON array.
Each element: {{"measure": int, "pitch": "C4", "duration": "quarter|half|whole|eighth|16th", "has_ornament": bool}}
Return ONLY the JSON array. No explanation, no markdown.

MusicXML:
{xml}"""

STEP2_PROMPTS = {
    "easier": """You are a music arranger. Given this note list, create a transformation plan to make the piece EASIER.
Rules:
- Replace 16th/32nd notes with eighth or quarter notes
- Remove ornaments (set has_ornament to false)
- Simplify dotted rhythms to straight rhythms

Note list:
{notes}

Return a JSON array of changes. Each change:
{{"measure": int, "pitch": "C4", "old_duration": "16th", "new_duration": "eighth", "remove_ornament": true}}
Return ONLY the JSON array. No explanation, no markdown.""",

    "harder": """You are a music arranger. Make the piece harder while keeping the melody clearly recognizable.

Key rule: The original melody note MUST stay on the beat (first position). Add ornamental notes AFTER it within the same duration.

For EVERY quarter note → [melody note as 16th, passing up as 16th, passing down as 16th, melody note as 16th]
For EVERY half note → [melody note as quarter, neighbor up as eighth, neighbor down as eighth, melody note as quarter — total = half]
For EVERY whole note → keep as whole note, add_ornament: true

Scale steps (use these for neighbors): C D E F G A B C(next octave)
Example: C4 quarter → [C4 16th, D4 16th, B3 16th, C4 16th] (melody C4 starts AND ends the group)

Note list:
{notes}

Return a JSON array with one entry per original note. No empty array. No explanation. No markdown.
Format: [{{"measure": 1, "original_pitch": "C4", "original_duration": "quarter", "new_notes": [{{"pitch": "C4", "duration": "16th"}}, {{"pitch": "D4", "duration": "16th"}}, {{"pitch": "B3", "duration": "16th"}}, {{"pitch": "C4", "duration": "16th"}}], "add_ornament": false}}]""",
}

STEP3_PROMPT = """You are a music engraver. Apply the transformation plan exactly to the original MusicXML.

Original MusicXML:
{xml}

Transformation plan (JSON):
{plan}

Rules:
- Apply every change in the plan exactly as specified
- Do NOT use <grace> elements — only regular <note> elements
- Update <divisions> if note durations change (quarter=2, eighth=1 when divisions=2)
- Keep all measures, key, time signature intact
- Return ONLY valid MusicXML. No markdown, no code fences, no explanation."""


async def transform(musicxml_content: str, difficulty: str = "easier") -> str:
    original_count = musicxml_content.count("<note>")
    print(f"\n{'='*40}")
    print(f"[Transform] difficulty={difficulty}, original notes={original_count}")
    print(f"{'='*40}")

    # Step 1: 음표 추출
    notes_json = _call(STEP1_PROMPT.format(xml=musicxml_content))
    print(f"[Step1] extracted notes:\n{notes_json[:400]}\n")

    # Step 2: 변환 계획 수립
    plan_json = _call(STEP2_PROMPTS[difficulty].format(notes=notes_json))
    print(f"[Step2] plan ({difficulty}):\n{plan_json[:400]}\n")

    # Step 3: 변환 계획 적용
    result = _call(STEP3_PROMPT.format(xml=musicxml_content, plan=plan_json))
    result_count = result.count("<note>")
    print(f"[Step3] result notes={result_count} (변화: {original_count} → {result_count})")
    print(f"{'='*40}\n")

    # 코드펜스 제거
    result = re.sub(r"^```[a-z]*\n", "", result.strip())
    result = re.sub(r"\n```$", "", result.strip())

    # grace note 제거 (OSMD가 처리 못함)
    result = re.sub(r"<note>\s*<grace[^>]*/>\s*.*?</note>", "", result, flags=re.DOTALL)
    grace_removed = musicxml_content.count("<note>") - result.count("<note>") if "<grace" in result else 0
    if grace_removed:
        print(f"[Post] grace notes removed: {grace_removed}")

    return result.strip()

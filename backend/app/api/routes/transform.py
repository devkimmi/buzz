from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.transform import TransformRequest, TransformResponse
from app.services import musicxml, llm

router = APIRouter()


@router.post("/transform", response_model=TransformResponse)
async def transform_score(
    file: UploadFile = File(...),
    difficulty: str = "easier",  # "easier" | "harder"
):
    content = await file.read()

    if not musicxml.is_valid(content):
        raise HTTPException(status_code=400, detail="Invalid MusicXML file")

    transformed = await llm.transform(content.decode(), difficulty=difficulty)

    return TransformResponse(musicxml=transformed)

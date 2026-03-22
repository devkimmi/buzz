import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from app.services import musicxml, llm

router = APIRouter()


@router.post("/transform")
async def transform_score(
    file: UploadFile = File(...),
    difficulty: str = Form("easier"),
):
    content = await file.read()

    if not musicxml.is_valid(content):
        raise HTTPException(status_code=400, detail="Invalid MusicXML file")

    async def event_stream():
        async for event in llm.transform(content.decode(), difficulty=difficulty):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

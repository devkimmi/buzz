from pydantic import BaseModel


class TransformRequest(BaseModel):
    difficulty: str = "easier"


class TransformResponse(BaseModel):
    musicxml: str

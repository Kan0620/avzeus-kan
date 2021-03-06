from pydantic import BaseModel, Field, StrictStr


class PredictRequest(BaseModel):
    input_text: str = Field(..., title="input_text", description="Input text", example="Input text for ML")

class CutResponse(BaseModel):
    result: dict = Field(..., title="result", description="Predict value", example={"is_face": False, "img": "None"})

class PredictResponse(BaseModel):
    result: dict = Field(..., title="result", description="Predict value", example={"rec_actress_id": "None"})

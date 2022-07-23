from typing import Any

from fastapi import APIRouter, Request

from models.predict import PredictRequest, CutResponse, PredictResponse

api_router = APIRouter()


@api_router.post("/cut", response_model=CutResponse)
async def predict(request: Request, payload: PredictRequest) -> Any:
    """
    ML Prediction API
    """
    input_text = payload.input_text
    # model = request.app.state.model

    # predict_value = model.cut(input_text)
    predict_value = request.app.state.model.cut(input_text)
    return PredictResponse(result=predict_value)

@api_router.post("/predict", response_model=PredictResponse)
async def predict(request: Request, payload: PredictRequest) -> Any:
    """
    ML Prediction API
    """
    input_text = payload.input_text
    # model = request.app.state.model

    # predict_value = model.predict(input_text)
    predict_value =request.app.state.model.predict(input_text)
    return PredictResponse(result=predict_value)



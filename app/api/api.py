from typing import Any
import random

from fastapi import APIRouter, Request


from app.models.predict import PredictRequest, CutResponse, PredictResponse, MovRecResponse

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

@api_router.post("/mov-rec", response_model=MovRecResponse)
async def predict(request: Request, payload: PredictRequest) -> Any:
    input_text = payload.input_text
    result = {}
    if input_text == "init":
        all_ids = list(request.app.state.mov_dict.keys())
        #random.shuffle(all_ids)
        mov_id = all_ids[0]
        ids = all_ids[1:11]
        result["movie"] = {
            "content_id": mov_id,
            "title": request.app.state.mov_dict[mov_id]["title"],
            "movieURL": request.app.state.mov_dict[mov_id]["movieURL"],
            "affiliateURL": request.app.state.mov_dict[mov_id]["affiliateURL"]
        }
        
    else:
        ids = request.app.state.mov_id_set
        saw_mov_ids = input_text.split("-")
        ids -= set(saw_mov_ids)
        ids = list(ids)
        print(ids)
        #random.shuffle(ids)
        ids = ids[:10]
        mov_id = saw_mov_ids[-1]
        result["movie"] = {
            "content_id": mov_id,
            "title": request.app.state.mov_dict[mov_id]["title"],
            "movieURL": request.app.state.mov_dict[mov_id]["movieURL"],
            "affiliateURL": request.app.state.mov_dict[mov_id]["affiliateURL"]
        }
        
    result["thumbnails"] = []
    print(len(ids))
    for id in ids:
        result["thumbnails"].append(
            {
                "content_id": id,
                "title": request.app.state.mov_dict[id]["title"],
                "imageURL": request.app.state.mov_dict[id]["imageURL"],
            }
        )

    return PredictResponse(result=result)




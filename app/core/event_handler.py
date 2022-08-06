from typing import Callable
import os

from fastapi import FastAPI
import requests

from app.services.model import MLModel


def _startup_model(app: FastAPI, model_path: str) -> None:
    model_instance = MLModel(model_path)
    app.state.model = model_instance
    URL = "https://api.dmm.com/affiliate/v3/ItemList?site=FANZA&sort=rank&hits=100"
    URL += ("&api_id=" + os.environ["API_ID"])
    URL += ("&affiliate_id=" + os.environ["AFFILIATE_ID"])
    mov_ids = []
    mov_dict = {}
    print("ml ok")
    for i in range(1):
        r = requests.get(URL + f"&offset={i+1}")
        for item in r.json()["result"]["items"]:
            if ("imageURL" in item.keys()) and ("sampleMovieURL" in item.keys())\
                and ("title" in item.keys())and ("content_id" in item.keys()):
                    if ("large" in item["imageURL"].keys()) and ("size_720_480" in item["sampleMovieURL"].keys()):
                        content_id = item["content_id"]
                        url = f"https://cc3001.dmm.co.jp/litevideo/freepv/{content_id[0]}/{content_id[:3]}/{content_id}/{content_id}_dmb_w.mp4"
                        status_code = requests.get(url).status_code
                        if str(status_code) == "200":
                            mov_ids.append(item["content_id"])
                            mov_dict[item["content_id"]] = {
                                "title": item["title"],
                                "imageURL": item["imageURL"]["large"],
                                "movieURL": item["sampleMovieURL"]["size_720_480"],
                            }
    app.state.mov_id_set = set(mov_ids)
    app.state.mov_dict = mov_dict



def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def start_app_handler(app: FastAPI, model_path: str) -> Callable:
    def startup() -> None:
        _startup_model(app, model_path)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        _shutdown_model(app)

    return shutdown

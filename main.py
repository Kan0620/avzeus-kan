from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from api.api import api_router
from api.heartbeat import heartbeat_router
from core.config import settings
from core.event_handler import start_app_handler, stop_app_handler


"""
origins = ["http://test-zeus-kan.s3-website-ap-northeast-1.amazonaws.com"]

middleware = [
    Middleware(CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    allow_origins=origins)]
"""
origins = [
    "http://test-zeus-kan.s3-website-ap-northeast-1.amazonaws.com",
    "https://avzeus-front.herokuapp.com/"]

middleware = [
    Middleware(CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["X-Requested-With", "Origin", "X-Csrftoken", "Content-Type", "Accept"],
    allow_origins=origins)]

app = FastAPI(middleware=middleware, title=settings.PROJECT_NAME)


app.include_router(heartbeat_router)
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["ML API"])

app.add_event_handler("startup", start_app_handler(app, settings.MODEL_PATH))
app.add_event_handler("shutdown", stop_app_handler(app))
"""

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
"""
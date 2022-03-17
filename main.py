from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from api.api import api_router
from api.heartbeat import heartbeat_router
from core.config import settings
from core.event_handler import start_app_handler, stop_app_handler

origins = [
    "http://localhost:3001/",
    "http://localhost:3001"
]
middleware = [Middleware(CORSMiddleware, allow_origins=origins)]

app = FastAPI(middleware=middleware, title=settings.PROJECT_NAME)


app.include_router(heartbeat_router)
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["ML API"])

app.add_event_handler("startup", start_app_handler(app, settings.MODEL_PATH))
app.add_event_handler("shutdown", stop_app_handler(app))
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
"""
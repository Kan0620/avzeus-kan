from fastapi import APIRouter

heartbeat_router = APIRouter()


@heartbeat_router.get("/", status_code=200)
def healthz() -> dict:
    """
    Healthz
    """
    return {"status": "OK"}

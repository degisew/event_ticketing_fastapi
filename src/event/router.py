from src.event.routes.event import router as event_router
from fastapi.routing import APIRouter


router = APIRouter()

router.include_router(event_router)

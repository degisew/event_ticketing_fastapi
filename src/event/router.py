from fastapi.routing import APIRouter
from src.event.routes.event import router as event_router
from src.event.routes.reservation import router as reservation_router


router = APIRouter()

router.include_router(event_router)
router.include_router(reservation_router)

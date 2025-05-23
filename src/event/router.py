from src.event.routes.event import router as event_router
from src.event.routes.ticket_type import router as ticket_type_router
from src.event.routes.reservation import router as reservation_router
from fastapi.routing import APIRouter


router = APIRouter()

router.include_router(event_router)
router.include_router(ticket_type_router)
router.include_router(reservation_router)

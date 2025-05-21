# from fastapi.routing import APIRouter
# from src.core.db import DbSession
# from src.event.schemas.ticket import TicketTypeResponseSchema, TicketTypeSchema
# from src.event.services.ticket_type import TicketTypeService


# router = APIRouter(prefix="/ticket_types")


# @router.post("/")
# async def create_ticket_types(
#     db: DbSession, payload: TicketTypeSchema
# ) -> TicketTypeResponseSchema:
#     return TicketTypeService.create_ticket_types(db, payload)


# @router.get("/")
# async def get_ticket_types(db: DbSession) -> list[TicketTypeResponseSchema]:
#     return TicketTypeService.get_ticket_types(db)


# @router.get("/{ticket_type_id}")
# async def get_ticket_type(db: DbSession, ticket_type_id) -> TicketTypeResponseSchema:
#     return TicketTypeService.get_ticket_type(db, ticket_type_id)


# @router.patch("/{ticket_type_id}")
# async def update_ticket_type(
#     db: DbSession, ticket_type: TicketTypeResponseSchema, ticket_type_id
# ) -> TicketTypeResponseSchema:
#     return TicketTypeService.update_ticket_type(db, ticket_type, ticket_type_id)

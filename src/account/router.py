from fastapi import APIRouter
from src.account.routers.users import router as users_router
from src.account.routers.roles import router as roles_router

router = APIRouter()

router.include_router(users_router)
router.include_router(roles_router)

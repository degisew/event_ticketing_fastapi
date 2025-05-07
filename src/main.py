from fastapi import FastAPI
from src.auth.routes import router as auth_router
from src.core.routes import router as core_router
from src.account.router import router as account_router
from src.payment.routes import router as payment_router
from src.event.router import router as event_router
from src.core.exceptions import register_global_exceptions


app = FastAPI()


app.include_router(core_router, prefix="/api/v1/core", tags=["Core"])
app.include_router(account_router, prefix="/api/v1/account")
app.include_router(event_router, prefix="/api/v1", tags=["Event"])
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(payment_router, prefix="/api/v1", tags=["Event"])

register_global_exceptions(app)

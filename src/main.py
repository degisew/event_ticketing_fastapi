from fastapi import FastAPI
from src.account.router import router as account_router
from src.event.router import router as event_router
from src.core.exceptions import register_global_exceptions


app = FastAPI()


app.include_router(account_router, prefix="/account")
app.include_router(event_router, tags=["Event"])


register_global_exceptions(app)

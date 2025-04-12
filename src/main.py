from fastapi import FastAPI
from src.account.router import router as account_router
from src.core.exceptions import register_global_exceptions


app = FastAPI()


app.include_router(account_router, prefix="/account")


register_global_exceptions(app)

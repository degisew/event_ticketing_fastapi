from fastapi import FastAPI
from src.account.router import router as account_router

# from src.core.db import create_db_and_tables


app = FastAPI()


app.include_router(account_router, prefix="/account")


# create_db_and_tables()

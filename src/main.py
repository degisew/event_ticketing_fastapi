from fastapi import FastAPI
from src.account import routes as account_routes


app = FastAPI()


app.include_router(account_routes.router)

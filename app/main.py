
from fastapi import FastAPI

from .routers import creditcard, debitcard, bankslip, callback
from .database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(callback.router)
app.include_router(creditcard.router)
app.include_router(debitcard.router)
app.include_router(bankslip.router)


@app.get("/")
def root():
    return {"Hello": "World"}

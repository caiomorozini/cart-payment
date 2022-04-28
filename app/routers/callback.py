from fastapi import (APIRouter, HTTPException, status)
from app import database
from app.functions import get_sale_cielo

router = APIRouter(
    prefix="/v1/callback",
    tags=["callback"]
)


@router.get("/{id}")
async def get_payment(id: str):
    payment = database.payments.select().where(database.payments.c.id == id)
    selected_id = await database.database.fetch_all(payment)
    if not selected_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"payment with id: {id} was not found")
    return selected_id


@router.get("/cielo_status/{id}")
async def payment_request(id: str):
    payment = database.payments.select().where(database.payments.c.id == id)
    selected_id = await database.database.fetch_all(payment)
    if not selected_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"payment with id: {id} was not found")

    return get_sale_cielo(selected_id[0]["response_cielo"])

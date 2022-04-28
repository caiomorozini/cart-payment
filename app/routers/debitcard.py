import logging
from fastapi import (APIRouter, HTTPException, Response, status)
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from app import schemas
from app.database import database, payments
from app.functions import cielo_create_sale, create_sale

router = APIRouter(
    prefix="/v1/debitcard",
    tags=["debitcard"]
)


@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.PaymentResponse)
async def create_payment(payment: schemas.DebitCard):
    sale = create_sale(payment, payment.type)
    response_cielo = cielo_create_sale(sale)
    logging.info("Pagamento criado")
    query = payments.insert().values(
        type=payment.type,
        response_cielo=response_cielo,
    )
    id = await database.execute(query)
    return {
        'id': id, 'payload': payment.dict(),
        'response_cielo': response_cielo
    }


@router.put("/{id}", status_code=HTTP_202_ACCEPTED, response_model=schemas.PaymentResponse)
async def update_payment(id: str, updated_payment: schemas.DebitCard) -> dict:
    updated_sale = create_sale(updated_payment, updated_payment.type)
    updated_response = cielo_create_sale(updated_sale)
    selected_payment = payments.select().where(payments.c.id == id)
    selected_id = await database.fetch_all(selected_payment)
    if not selected_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'payment with id: {id} does not exist'
        )
    else:
        payment = payments.update().where(payments.c.id == id).values(response_cielo=updated_response)
        selected_id = await database.execute(payment)
        logging.info('updated payment')

    return {
        "id": id, 'payload': updated_payment,
        "response_cielo": updated_response
    }


@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
async def delete_payment(id: str):
    payment = payments.select().where(payments.c.id == id)
    selected_id = await database.fetch_all(payment)
    if selected_id == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'payment with id: {id} does not exist')
    else:
        payment = payments.delete().where(payments.c.id == id)

        logging.info('payment deleted')

        await database.fetch_all(payment)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

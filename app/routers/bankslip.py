from app.functions import cielo_create_sale, create_sale
from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED
from app import schemas
from app.database import database, payments


router = APIRouter(
    prefix="/v1/bankslip",
    tags=["bankslip"]
)


@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.PaymentResponse)
async def create_payment(payment: schemas.BankSlip):
    sale = create_sale(payment, payment.type)
    response_cielo = cielo_create_sale(sale)
    query = payments.insert().values(
        type=payment.type,
        response_cielo=response_cielo,
    )
    id = await database.execute(query)

    return {
        'id': id, 'payload': payment.dict(),
        'response_cielo': response_cielo
    }

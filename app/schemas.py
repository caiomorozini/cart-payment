from typing import Optional
from cieloApi3.payment import PROVIDER_BANCO_DO_BRASIL
from pydantic import BaseModel, validator
from pydantic.types import conint, constr, PaymentCardBrand, PaymentCardNumber
from datetime import date, datetime

from .const import *


class PaymentBase(BaseModel):
    merchant_order_id: constr(
        regex=REGEX_MERCHANT_ORDER_ID, max_length=LEN_MAX_MERCHANT_ORDER_ID) = "1234512345"
    customer_name: Optional[constr(
        strip_whitespace=True, max_length=LEN_MAX_CUSTOMER_NAME)] = 'Nome Padrao'
    amount: conint(gt=MIN_AMOUNT, lt=MAX_AMOUNT) = 15700


class Card(BaseModel):
    holder: constr(
        strip_whitespace=True, min_length=LEN_MIN_HOLDER) = "Holder Name"
    card_number: PaymentCardNumber = "5277696455399733"
    expiration_date: constr(
        max_length=LEN_MAX_EXPIRATION_DATE, regex=REGEX_EXPIRATION_DATE) = "01/2028"
    security_code: constr(max_length=LEN_MAX_SECURITY_CODE) = "123"

    # Required to validate if the date is expired
    @validator('expiration_date')
    def expired(cls, value) -> str:
        exp_date = datetime.strptime(value, '%m/%Y').date()
        if exp_date < date.today():
            raise ValueError('Expired date')
        return value

    @property
    def brand(self) -> PaymentCardBrand:
        if self.card_number.brand == 'Mastercard':
            return 'Master'
        elif self.card_number.brand == 'American Express':
            return 'Amex'
        else:
            return self.card_number.brand


class CreditCard(PaymentBase, Card):
    type: constr(max_length=LEN_MAX_TYPE) = 'CreditCard'
    installments: conint(gt=MIN_INSTALLMENTS, lt=MAX_INSTALLMENTS) = 1


class DebitCard(PaymentBase, Card):
    type: constr(max_length=LEN_MAX_TYPE) = 'DebitCard'
    authenticate: bool = True
    return_url: constr(strip_whitespace=True, max_length=1024)


class BankSlip(PaymentBase):
    type: constr(max_length=LEN_MAX_TYPE) = 'Boleto'

    # Customer Adress
    street: constr(max_length=LEN_MAX__ADRESS_STREET) = "Alameda Xingu"
    number: constr(max_length=LEN_MAX_ADRESS_NUMBER) = "512"
    complement: Optional[str]
    zip_code: constr(max_length=LEN_MAX_ADRESS_ZIP_CODE) = "12345987"
    district: constr(max_length=LEN_MAX_ADRESS_DISTRICT) = "Alphaville"
    city: constr(max_length=LEN_MAX_ADRESS_CITY) = "São Paulo"  # Bradesco: 50 / BB: 18
    state: constr(max_length=LEN_MAX_ADRESS_STATE) = 'SP'
    country: constr(max_length=LEN_MAX_ADRESS_COUNTRY) = "BRA"

    # Payment
    provider: constr(max_length=LEN_MAX_PROVIDER) = PROVIDER_BANCO_DO_BRASIL
    address: Optional[str]
    boleto_number: Optional[str]
    assignor: Optional[str]
    demonstrative: Optional[str]
    expiration_date: Optional[str]
    identification: Optional[constr(max_length=LEN_MAX_IDENTIFICATION)]
    instructions: Optional[constr(max_length=LEN_MAX_INSTRUCTIONS)]


class PaymentResponse(BaseModel):
    id: str
    response_cielo: dict
    payload: dict

    class Config:
        def __init__(self):
            pass

        orm_mode = True

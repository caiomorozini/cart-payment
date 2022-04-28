import cieloApi3
from logging import *
from cieloApi3 import payment
from .config import settings
from cieloApi3.payment import (
    PAYMENTTYPE_BOLETO, PAYMENTTYPE_CREDITCARD,
    PAYMENTTYPE_DEBITCARD, PROVIDER_BANCO_DO_BRASIL,
)


def create_sale(payload: dict, type: str):
    functions = {
        'CreditCard': create_payment_cards,
        'DebitCard': create_payment_cards,
        'Boleto': create_payment_boleto,
    }
    types = {
        'Creditcard': PAYMENTTYPE_CREDITCARD,
        'DebitCard': PAYMENTTYPE_DEBITCARD,
        'Boleto': PAYMENTTYPE_BOLETO,
    }

    sale = cieloApi3.Sale(payload.merchant_order_id)
    sale.customer = cieloApi3.Customer(payload.customer_name)
    selected_function = functions.get(type)
    sale.payment = selected_function(payload, types.get(type))
    return sale


def create_payment_cards(payload: dict, type: str) -> object:
    card = create_card(
        payload.card_number,
        payload.holder,
        payload.security_code,
        payload.brand,
        payload.expiration_date,
    )
    if type == PAYMENTTYPE_DEBITCARD:
        payment = create_payment(
            type,
            payload.amount,
            return_url=payload.return_url,
        )
        payment.debit_card = card

    else:
        payment = create_payment(
            type,
            payload.amount,
            payload.installments,
        )
        payment.credit_card = card
    return payment


def create_payment_boleto(payload: dict, type) -> object:
    payment = cieloApi3.Payment(payload.amount)
    payment.type = type
    payment.provider = PROVIDER_BANCO_DO_BRASIL
    payment.address = payload.address
    payment.boleto_number = payload.boleto_number
    payment.assignor = payload.assignor
    payment.demonstrative = payload.demonstrative
    payment.expiration_date = payload.expiration_date
    payment.identification = payload.identification
    payment.instructions = payload.instructions
    return payment


def create_payment(
        payment_type: str, amount: int,
        installments: int = 1, **kwargs) -> object:

    payment = cieloApi3.Payment(amount, installments)
    payment.type = payment_type
    if payment_type == PAYMENTTYPE_DEBITCARD:
        payment.authenticate = True
        payment.return_url = kwargs.get('return_url')
    return payment


def create_card(
        card_number: str,
        holder: str,
        security_code: str,
        brand: str,
        expiration_date: str) -> object:

    card = cieloApi3.CreditCard(security_code, brand)
    card.expiration_date = expiration_date
    card.card_number = card_number
    card.holder = holder
    return card


def cielo_create_sale(sale: object) -> dict:
    cielo_ecommerce = connect_cielo()
    response_create_sale = cielo_ecommerce.create_sale(sale)
    info(f'{sale.payment.type} sale created')
    payment_id = sale.payment.payment_id
    if sale.payment.type == PAYMENTTYPE_CREDITCARD:
        message_status = response_create_sale['Payment']['ReturnMessage']
        info(message_status)
        if not message_status == 'Operation Sucessful':
            # Necessary to verify that the data is valid to perform the capture
            return {
                'response_create_sale': response_create_sale,
                'capture_response': message_status,
            }
        response_capture_sale = cielo_ecommerce.capture_sale(payment_id, amount=payment.amount)
        return {'response_capture_sale': response_create_sale,
                'capture_response': response_capture_sale}
    return {'response_create_sale': response_create_sale}


def connect_cielo() -> object:
    environment = cieloApi3.Environment(sandbox=True)
    merchant = cieloApi3.Merchant(settings.merchant_id, settings.merchant_key)
    cielo_ecommerce = cieloApi3.CieloEcommerce(merchant, environment)
    return cielo_ecommerce


def get_sale_cielo(sale: dict) -> dict:
    cielo_ecommerce = connect_cielo()
    id = sale['response_create_sale']['Payment']['PaymentId']
    return cielo_ecommerce.get_sale(id)


def cancel_sale(sale: dict) -> dict:
    cielo_ecommerce = connect_cielo()
    id = sale['response_create_sale']['Payment']['PaymentId']
    amount = sale['response_create_sale']['Payment']['Amount']
    return cielo_ecommerce(id, amount)

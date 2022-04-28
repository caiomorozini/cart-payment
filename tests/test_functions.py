from pydantic.main import BaseModel
from app.functions import cielo_create_sale, create_sale


class PayloadCreditCard(BaseModel):
    merchant_order_id = "2014111703"
    type = "CreditCard"
    customer_name = "Test Customer"
    amount = 20100
    installments = 12
    card_number = None,  # Need to specify for each test
    expiration_date = "12/2028"
    holder = "Test Holder"
    security_code = "456"
    brand = "Visa"


class PayloadDebitCard(BaseModel):
    merchant_order_id = "2014111703"
    type = "DebitCard"
    customer_name = "Test Customer"
    amount = 20000
    card_number = None,  # Need to specify for each test
    expiration_date = "01/2028"
    holder = "Test Holder"
    security_code = "123"
    brand: str = None
    return_url = "https://www.cielo.com.br/"


credit_payload = PayloadCreditCard()
debit_payload = PayloadDebitCard()


def test_cielo_debit_card_sucess():
    debit_payload.card_number = "5555666677778884"
    debit_payload.brand = "Master"
    debit_payload.expiration_date = "12/2022"
    sale = create_sale(debit_payload, debit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    status = response['Payment']['Status']
    assert return_code == "1"
    assert status == 0


def test_cielo_sucess_operation():
    credit_payload.card_number = "0000.0000.0000.0001"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == '4' or '6'
    assert return_message == 'Operation Successful'


def test_cielo_not_authorized():
    credit_payload.card_number = "0000.0000.0000.0002"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == "05"
    assert return_message == "Not Authorized"


def test_cielo_expired_card():
    credit_payload.card_number = "0000.0000.0000.0003"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == "57"
    assert return_message == "Card Expired"


def test_cielo_blocked_card():
    credit_payload.card_number = "0000.0000.0000.0005"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == "78"
    assert return_message == "Blocked Card"


def test_cielo_time_out():
    credit_payload.card_number = "0000.0000.0000.0006"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == "99"
    assert return_message == "Timeout"


def test_cielo_card_canceled():
    credit_payload.card_number = "0000.0000.0000.0007"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == "77"
    assert return_message == "Card Canceled"


def test_cielo_problem_card():
    credit_payload.card_number = "0000.0000.0000.0008"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == "70"
    assert return_message == "Problems with Creditcard"


def test_cielo_random_card():
    credit_payload.card_number = "0000.0000.0000.0009"
    sale = create_sale(credit_payload, credit_payload.type)
    response_cielo = cielo_create_sale(sale)
    response = response_cielo['response_create_sale']
    return_code = response['Payment']['ReturnCode']
    return_message = response['Payment']['ReturnMessage']
    assert return_code == "99" or "4"
    assert return_message == "Operation Successful" or "Timeout"

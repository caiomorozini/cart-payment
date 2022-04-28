from starlette.testclient import TestClient
from app.main import app
from app.schemas import PaymentResponse
from faker import Faker

fake = Faker(locale="pt_BR")  # Creates an object containing valid credit card

PAYLOAD = {
    "merchant_order_id": "2014111703",
    "type": "CreditCard",
    "customer_name": "Test Customer",
    "amount": 20100,
    "installments": 12,
    "card_number": None,  # Need to specify for each test
    "expiration_date": "12/2022",
    "holder": "Test Holder",
    "security_code": "456"
}

router = "/v1/creditcard/"


def test_sucess_payment():
    PAYLOAD["card_number"] = fake.credit_card_number(card_type='visa')
    with TestClient(app) as client:
        response = client.post(f"{router}", json=PAYLOAD)
    payment_response = PaymentResponse(**response.json())

    assert response.status_code == 201
    assert payment_response.payload == PAYLOAD


def test_failure_payment():
    PAYLOAD["card_number"] = '0000.O000.0000.1234'
    with TestClient(app) as client:
        response = client.post(f"{router}", json=PAYLOAD)
    assert response.status_code == 422


def test_update_payment():
    PAYLOAD["card_number"] = fake.credit_card_number(card_type='visa')
    PAYLOAD["customer_name"] = "Op without update"
    with TestClient(app) as client:
        first_response = client.post(f"{router}", json=PAYLOAD)
        payment = PaymentResponse(**first_response.json())
        id = payment.id

        PAYLOAD["customer_name"] = "Op with update"
        second_response = client.put(f"{router}{id}", json=PAYLOAD)

        updated_payment = PaymentResponse(**second_response.json())

    assert first_response.status_code == 201
    assert payment.response_cielo['response_create_sale']['Customer']['Name'] == (
        "Op without update"
    )
    assert second_response.status_code == 202
    assert "Op with update" == \
           (
               updated_payment.response_cielo['response_create_sale']["Customer"]["Name"]
           )


def test_delete_payment():
    PAYLOAD["card_number"] = fake.credit_card_number(card_type='amex')
    with TestClient(app) as client:
        old_response = client.post(
            f"{router}",
            json=PAYLOAD
        )
        new_payment = PaymentResponse(**old_response.json())
        id = new_payment.id
        response = client.delete(
            f"{router}{id}",
            json=PAYLOAD,
        )
    assert old_response.status_code == 201
    assert response.status_code == 204

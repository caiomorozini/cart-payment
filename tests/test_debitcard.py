from starlette.testclient import TestClient
from app.main import app
from faker import Faker
from app.schemas import PaymentResponse

fake = Faker(locale="pt_BR")  # Creates an object containing valid credit card
PAYLOAD = \
    {
        "merchant_order_id": "1234512345",
        "customer_name": "Customer test",
        "amount": 15700,
        "type": "DebitCard",
        "authenticate": True,
        "card_number": fake.credit_card_number(card_type='visa'),
        "expiration_date": "10/2029",
        "holder": "Customer D Test",
        "security_code": "123",
        "return_url": "url",
    }

router = "/v1/debitcard/"


def test_create_debit_payment_sucess():
    with TestClient(app) as client:
        response = client.post(
            f"{router}",
            json=PAYLOAD
        )
    assert response.status_code == 201


def test_failure_payment():
    PAYLOAD["card_number"] = 'str123'
    with TestClient(app) as client:
        response = client.post(f"{router}", json=PAYLOAD)
    assert response.status_code == 422


def test_update_payment():
    PAYLOAD["card_number"] = fake.credit_card_number(card_type='mastercard')
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

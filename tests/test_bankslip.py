from starlette.testclient import TestClient
from app.main import app

PAYLOAD = {
    "merchant_order_id": "2014111706",
    "customer_name": "Comprador Teste Boleto",
    "identity": "1234567890",
    "street": "Avenida Marechal Câmara",
    "number": "160",
    "complement": "Sala 934",
    "zip_code": "22750012",
    "district": "Centro",
    "city": "Rio de Janeiro",
    "state": "RJ",
    "country": "BRA",
    "type": "Boleto",
    "amount": 15700,
    "address": "Rua Teste",
    "boleto_number": "123",
    "assignor": "Empresa Teste",
    "demonstrative": "Desmonstrative Teste",
    "expiration_date": "2023-12-31",
    "identification": "11884926754",
    "instructions": "Aceitar somente até a data de vencimento, \
    após essa data juros de 1 dia.",
}

router = "/v1/bankslip/"


def test_create_payment():
    with TestClient(app) as client:
        response = client.post(
            f"{router}",
            json=PAYLOAD
        )
    assert response.status_code == 201

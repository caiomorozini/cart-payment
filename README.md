# Instalar todos os pacotes

```
poetry install
```

# Rodar os testes

```
poetry run pytest tests/ -v -x
```


# Iniciar o servidor

```
poetry run uvicorn app.main:app --reload
```

# Acessar os docs

Dps de iniciar o servidor visite o endereço:

```
http://127.0.0.1:8000/docs#/
```
# Acessar flake8 
```
poetry run flake8  
```
## Configurações Adicionais do flake8
### Para verificar erros de estilo no commit:
```
flake8 --install-hook git
```
### Bloquear os commits quando houver um erro:
```
git config--bool flake8.strict true
```
# Notificação de eventos
MEIO DE PAGAMENTO|EVENTO
-|-
Cartão de Crédito|Captura
Cartão de Crédito|Cancelamento
Cartão de Crédito|Sondagem
Boleto|Conciliação
Boleto|Cancelamento Manual
Transferência eletrônica|Confirmadas

# Contract example (Credit card)

```json
{
  "merchant_order_id": "2014111703",
  "payment": {
    "type": "CreditCard",
    "amount": 15700,
    "installments": 1,
    "credit_card": {
      "card_number": "4551870000000183",
      "expiration_date": "12/2021",
      "brand": "Visa"
    }
  }
}

```
# Contract example (Debit card)
```json
{  
   "MerchantOrderId":"2014121201",
   "Customer":{  
      "Name":"Comprador Cartão de débito"
   },
   "Payment":{  
     "Type":"DebitCard",
     "Authenticate": true,
     "Amount":15700,
     "ReturnUrl":"http://www.cielo.com.br",
     "DebitCard":{  
         "CardNumber":"4551870000000183",
         "Holder":"Teste Holder",
         "ExpirationDate":"12/2030",
         "SecurityCode":"123",
         "Brand":"Visa"
     },
     "IsCryptoCurrencyNegotiation": true
   }
}
```
## Curl Example

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/payments/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "merchant_order_id": "2014111703",
  "type": "CreditCard",
  "customer_name": "15700",
  "amount": 15700,
  "installments": 1,
  "card_number": "4551870000000183",
  "expiration_date": "12/2021",
  "holder": "string",
  "brand": "Visa",
  "security_code": "123"
}'
```


# Cielo response (creditcard)

~~~json
{
    "MerchantOrderId": "2014111706",
    "Customer": {
        "Name": "Comprador crédito simples"
    },
    "Payment": {
        "ServiceTaxAmount": 0,
        "Installments": 1,
        "Interest": "ByMerchant",
        "Capture": false,
        "Authenticate": false,
        "CreditCard": {
            "CardNumber": "455187******0183",
            "Holder": "Teste Holder",
            "ExpirationDate": "12/2030",
            "SaveCard": false,
            "Brand": "Visa",
            "CardOnFile":{
               "Usage": "Used",
               "Reason":"Unscheduled"
            }
        },
        "IsCryptoCurrencyNegotiation": true,
        "tryautomaticcancellation":true,
        "ProofOfSale": "674532",
        "Tid": "0305023644309",
        "AuthorizationCode": "123456",
        "PaymentId": "24bc8366-fc31-4d6c-8555-17049a836a07",
        "Type": "CreditCard",
        "Amount": 15700,
        "Currency": "BRL",
        "Country": "BRA",
        "ExtraDataCollection": [],
        "Status": 1,
        "ReturnCode": "4",
        "ReturnMessage": "Operation Successful",
        "Links": [
            {
                "Method": "GET",
                "Rel": "self",
                "Href": "https://apiquerysandbox.cieloecommerce.cielo.com.br/1/sales/{PaymentId}"
            },
            {
                "Method": "PUT",
                "Rel": "capture",
                "Href": "https://apisandbox.cieloecommerce.cielo.com.br/1/sales/{PaymentId}/capture"
            },
            {
                "Method": "PUT",
                "Rel": "void",
                "Href": "https://apisandbox.cieloecommerce.cielo.com.br/1/sales/{PaymentId}/void"
            }
        ]
    }
}
~~~
# Cielo response (ticket)
~~~json
{  
    "MerchantOrderId":"2014111706",
    "Customer":
    {  
        "Name":"Comprador Teste Boleto",
        "Identity": "1234567890",
        "Address":
        {
          "Street": "Avenida Marechal Câmara",
          "Number": "160",    
          "Complement": "Sala 934",
          "ZipCode" : "22750012",
          "District": "Centro",
          "City": "Rio de Janeiro",
          "State" : "RJ",
          "Country": "BRA"
        }
    },
    "Payment":
    {  
        "Type":"Boleto",
        "Amount":15700,
        "Provider":"INCLUIR PROVIDER",
        "Address": "Rua Teste",
        "BoletoNumber": "123",
        "Assignor": "Empresa Teste",
        "Demonstrative": "Desmonstrative Teste",
        "ExpirationDate": "2020-12-31",
        "Identification": "11884926754",
        "Instructions": "Aceitar somente até a data de vencimento, após essa data juros de 1% dia."
    }
}
~~~
# Mudanças Cielo3

./cieloApi3/requests/base

~~~python
54 | raise Exception('\r\n%s\r\nMethod: %s\r\nUri: %s\r\nData: %s' % (''.join(errors), method, response.url, json.dumps(data_send, indent=2)))
~~~

./ObjectJSON

~~~python
61 | if valor or isinstance(valor, (int, str, float, complex)):
~~~ 

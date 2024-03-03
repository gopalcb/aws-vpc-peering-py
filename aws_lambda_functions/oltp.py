"""
CODE FOR AWS LAMBDA FUNCTIONS
Author: Gopal
---

Keyword arguments:
argument -- 
    event['data'] = {
        'key': 'val'
    } 

Return --
    {
        'statusCode': 200,
        'body': json.dumps(output)
    }

"""

import boto3
import botocore
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

RETRY_COUNT = 0


def lambda_handler(event, context):
   try:
      data = event['data']
      card_holder_name = data['card_holder_name']
      cardno = data['cardno']
      exp = data['exp']
      code = data['code']
      amount = data['amount']
      data['status'] = 'processing'

      data = add_update_dynamodb_table(data, 'started')

      response = process_payment(data)

      return {
        'statusCode': 200,
        'data': response
      }
   
   except Exception as e:
      return {
        'statusCode': 400,
        'data': {}
      }
   

def add_update_dynamodb_table(data, action):
   """
   data: dict
        {
            '': ''
        }
    action: str ('add'/'update')

    return: bool (True/False)
   """
   
   try:
      pass
   
   except Exception as e:
      pass
   

def process_payment():
   try:
      pass
   
   except Exception as e:
      pass
   

def charge_credit_card(self, card, amount):
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = settings.get_api_login_id()
    merchant_auth.transactionKey = settings.get_transaction_id()
    
    credit_card = apicontractsv1.creditCardType()
    credit_card.cardNumber = card.number
    credit_card.expirationDate = card.expiration_date
    credit_card.cardCode = card.code
    
    payment = apicontractsv1.paymentType()
    payment.creditCard = credit_card
    
    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType ="authCaptureTransaction"
    transaction_request.amount = Decimal(amount)
    transaction_request.payment = payment
    
    request = apicontractsv1.createTransactionRequest()
    request.merchantAuthentication = merchant_auth
    request.refId ="MerchantID-0001"
    request.transactionRequest = transaction_request

    transaction_controller = createTransactionController(request)
    transaction_controller.execute()
    
    api_response = transaction_controller.getresponse()
    response = self.response_mapper(api_response)
    return response


def response_mapper(self, api_response):
    response = models.TransactionResponse()

    if api_response is None:
        response.messages.append("No response from api")
        return response
    
    if api_response.messages.resultCode=="Ok":
        response.is_success = hasattr(api_response.transactionResponse, 'messages')
        if response.is_success:
            response.messages.append(f"Successfully created transaction with Transaction ID: {api_response.transactionResponse.transId}")
            response.messages.append(f"Transaction Response Code: {api_response.transactionResponse.responseCode}")
            response.messages.append(f"Message Code: {api_response.transactionResponse.messages.message[0].code}")
            response.messages.append(f"Description: {api_response.transactionResponse.messages.message[0].description}")
        else:
            if hasattr(api_response.transactionResponse, 'errors') is True:
                response.messages.append(f"Error Code:  {api_response.transactionResponse.errors.error[0].errorCode}")
                response.messages.append(f"Error message: {api_response.transactionResponse.errors.error[0].errorText}")
        return response

    response.is_success = False
    response.messages.append(f"response code: {api_response.messages.resultCode}")

    return response
   

def handle_error():
   pass


def log(string):
   print(string)

import json
import os
import time
from pathlib import Path

import stripe
from dotenv import load_dotenv
from requests import session

BASE_DIR = Path(__file__).resolve().parent.parent



dotenv_path = Path(BASE_DIR /'website/.env')
load_dotenv(dotenv_path=dotenv_path)

STRIPE_PUBLIC_KEY =os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY =os.getenv('STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')


stripe.api_key = STRIPE_SECRET_KEY

# creating account
def create_account(STRIPE_SECRET_KEY,email,unix_datetime,user_ip_address):
  stripe.api_key = STRIPE_SECRET_KEY

  create_user = (stripe.Account.create(
    type="express",
    country="GB",
    email=email,
    capabilities={
      "card_payments": {"requested": True},
      "transfers": {"requested": True},
    },
    # tos_acceptance = {
    #   "date": unix_datetime,
    #   "ip": user_ip_address,
    # },
    # business_type="individual",
    # business_profile={
    #   "mcc":"8398",
    #   "url":"www.google1.com",
    # }

  ))

  return create_user["id"]

test_email = "TestingExpress@123.com"
unix_datetime = round(time.time())
user_ip_address = "127.0.0.1"

# * calling create_account
# print(create_account(STRIPE_SECRET_KEY,test_email,unix_datetime,user_ip_address))


def create_account_link(STRIPE_SECRET_KEY,stripe_id):
  stripe.api_key = STRIPE_SECRET_KEY

  link = stripe.AccountLink.create(
    account=stripe_id,
    refresh_url="http://localhost:3000",
    return_url="http://localhost:3000",
    type="account_onboarding",
  )

  return(link["url"])

# * calling create_account_link
# stripe_id = "acct_1LPoqgRIQJeOn4y3"
# print(create_account_link(STRIPE_SECRET_KEY,stripe_id))

def pop_user_data(STRIPE_SECRET_KEY,stripe_id):
  stripe.api_key = STRIPE_SECRET_KEY
  retrieve_account = stripe.Account.retrieve(stripe_id)
  return (retrieve_account)

# print(pop_user_data(STRIPE_SECRET_KEY,stripe_id))

def delete_account(STRIPE_SECRET_KEY,stripe_id):
  stripe.api_key = STRIPE_SECRET_KEY
  delete_statues = stripe.Account.delete(stripe_id)

  return delete_statues

# print(delete_account(STRIPE_SECRET_KEY,"acct_1LMvUhRK1ZjfoEz7"))



# * transfer_from_Oliver_McCourty_to_Speaker_in_stripe
def transfer_from_Oliver_McCourty_to_Speaker_in_stripe(STRIPE_SECRET_KEY,stripe_id,amount):
  stripe.api_key = STRIPE_SECRET_KEY
  transfer = stripe.Transfer.create(
    amount=amount,
    currency="gbp",
    destination=stripe_id,
  )

  return transfer

# * calling transfer_from_Oliver_McCourty_to_Speaker_in_stripe
stripe_id = "acct_1LPoqgRIQJeOn4y3"
amount = 1000
# print(transfer_from_Oliver_McCourty_to_Speaker_in_stripe(STRIPE_SECRET_KEY,stripe_id,amount))

# * create the product
Organiser_to_Speaker_product_id = "prod_MB0vrE8bnfdXmJ"
# print(stripe.Product.create(name="Organiser_to_Speaker"))

# * create price to product
# amount = 100000
def create_price(STRIPE_SECRET_KEY,amount,Organiser_to_Speaker_product_id):
  stripe.api_key = STRIPE_SECRET_KEY
  create_price = stripe.Price.create(
    unit_amount=amount,
    currency="gbp",
    product=Organiser_to_Speaker_product_id,
  )
  return create_price

# print(create_price(STRIPE_SECRET_KEY,amount,Organiser_to_Speaker_product_id))

# * payout 
def payout (STRIPE_SECRET_KEY,stripe_id,amount):
  stripe.api_key = STRIPE_SECRET_KEY
  payout = stripe.Payout.create(
    amount=amount,
    currency='gbp',
    stripe_account=stripe_id,
  )

  return payout
# * calling payout in Oliver account
amount = 1234
stripe_id = ""
# print(payout (STRIPE_SECRET_KEY,stripe_id,amount))

# * calling payout in Speaker account
# stripe_id = "acct_1LPoqgRIQJeOn4y3"
# amount = 100
# print(payout (STRIPE_SECRET_KEY,stripe_id,amount))

# product_id = "prod_M3XLtEy50ZuKEs"
# price_id = "price_1LLSzTIoOYLVzWlCTwxGFngY"

# creating a payment session one to one 

def create_payment_session(STRIPE_SECRET_KEY,price_id,success_url,cancel_url,stripe_account_id,application_fee_amount):
  stripe.api_key = STRIPE_SECRET_KEY

  session = stripe.checkout.Session.create(
    success_url=success_url,
    cancel_url=cancel_url,
    line_items=[
      {
        "price": price_id,
        "quantity": 1,
      },
    ],
    mode="payment",
    payment_intent_data={
    'application_fee_amount': application_fee_amount,
    'transfer_data': {
      'destination': stripe_account_id,
    }}
  )

  return session

success_url="http://localhost:3000/"
cancel_url="http://localhost:3000/"
price_id = "price_1LPiwrIUHPWGBvT8wu2b1rmR"
stripe_account_id = "acct_1LPoqgRIQJeOn4y3"
application_fee_amount = 5000
# * calling create_payment_session function
# print(create_payment_session(STRIPE_SECRET_KEY,price_id,success_url,cancel_url,stripe_account_id,application_fee_amount))



# *List all the connected account 
def list_all_connected_account (STRIPE_SECRET_KEY):
  stripe.api_key = STRIPE_SECRET_KEY
  connected_account = stripe.Account.list(limit=30)

  return connected_account.data

# ac_list = list_all_connected_account (STRIPE_SECRET_KEY)
# print(ac_list)
# print(ac_list[0]["id"])
# print(len(ac_list))

# white_list = [
#   "acct_1LY3oaRIBwSgRbzR",
#   "acct_1LY3j3RT1G1ZHMzJ",
#   "acct_1LXiEmRT59cdEb11",
#   "acct_1LXhJoRPZCQwloaY",
#   "acct_1LXSjiRBDKrUn0d4",
#   "acct_1LXShqRAGLY8FASs",
#   "acct_1LXSaWRKTxmGV7nb",
#   "acct_1LXRmbRCRJDQhbka",
#   "acct_1LXRexRS2YUFu1Ps",
#   "acct_1LXNcRRBwlzYRNXV",
#   "acct_1LXNNFRDTCZx5c6O",
#   "acct_1LXS4cRAoEzUCSmu",
#   # "acct_1LY5ZtRFSqweCPDx",
#   # "acct_1LY5YkRMwVLbGqMx"
#   ]



# for y in white_list:
#   for x in range (len(ac_list)) :
#     if ac_list[x].id != y :
#       print("this user not in white list")
#       print(ac_list[x].id)
#       print(delete_account(STRIPE_SECRET_KEY,ac_list[x].id))
#     else:
#       print("this user in white list !!!!!!!!!!!!!!!!!!!!!!!!!")
#       print(f"white list ac from stripe: {ac_list[x].id}" )
#       print(f"white list ac from python: {y}"  )
    
#     # print(ac_list[x].id)
# #   print(delete_account(STRIPE_SECRET_KEY,ac_list[x].id))


# * Retrieve a Session
def retrieve_Session(STRIPE_SECRET_KEY):
  stripe.api_key = STRIPE_SECRET_KEY
  session_id = "cs_test_a1pWr7QQHlcHMdODQABsLui6qatct1r4YTkEyNFsIOfeEYvKJ3bL0BbMy8"
  retrieve_Session = (stripe.checkout.Session.retrieve(session_id))

  return (retrieve_Session)

# * calling retrieve_Session
# print(retrieve_Session(STRIPE_SECRET_KEY))


# * retrieve a PaymentIntent
def retrieve_paymentIntent(STRIPE_SECRET_KEY,paymentIntent_id):
  stripe.api_key = STRIPE_SECRET_KEY
  paymentIntent = stripe.PaymentIntent.retrieve(paymentIntent_id)

  # print("payment_status")
  # print(paymentIntent["charges"]["data"][0]['paid'])

  return paymentIntent

# paymentIntent_id = "pi_3LNaVoIUHPWGBvT82VNdsnC6"
# print(retrieve_paymentIntent(STRIPE_SECRET_KEY,"pi_3LNbpIIUHPWGBvT812kBnPr9"))
# retrieve_paymentIntent(STRIPE_SECRET_KEY,paymentIntent_id)

# * check payment status
def check_payment_status(STRIPE_SECRET_KEY,paymentIntent_id):
  stripe.api_key = STRIPE_SECRET_KEY
  paymentIntent = stripe.PaymentIntent.retrieve(paymentIntent_id)

  # print("payment_status")
  payment_status = (paymentIntent["charges"]["data"][0]['paid'])

  return payment_status

paymentIntent_id = "pi_3LNaVoIUHPWGBvT82VNdsnC6"

# * calling check_payment_status
# print(check_payment_status(STRIPE_SECRET_KEY,paymentIntent_id))


# * list all the bank account
def list_bank_account(STRIPE_SECRET_KEY):
  stripe.api_key = STRIPE_SECRET_KEY
  bank_ac = stripe.Customer.list_sources(
  object="bank_account",
  limit=3,
  )
  return bank_ac 


# * Create log in link
def create_login_link(STRIPE_SECRET_KEY,stripe_id):
  stripe.api_key = STRIPE_SECRET_KEY
  account_link = stripe.Account.create_login_link(stripe_id)

  return account_link["url"]

# *calling Create log in link
stripe_id = "acct_1LPqH1RBe7l0Njzm"
# print(create_login_link(STRIPE_SECRET_KEY,stripe_id))


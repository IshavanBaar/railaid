#!/usr/bin/python
from flask import Flask, session, render_template, url_for, redirect, request, flash, g
from flask.ext import assets
import json
import os
import paypalrestsdk

app = Flask(__name__)
paypal_client_id = "AacMHTvbcCGRzaeuHY6i6zwqGvveuhN4X_2sZ2mZJi76ZGtSZATh7XggfVuVixzyrRuG-bJTLOJIXltg"
paypal_client_secret = "EOLqrOVlYbzBeQIXIu_lQiB2Idh7fpK71hemdmlrfV1UwkW9EfDIuHOYS9lZYcxDKj4BzKO08b-CdDt9"

#Assets
env = assets.Environment(app)
env.load_path = [
  os.path.join(os.path.dirname(__file__), 'assets')
]

env.register (
    'js_all',
    assets.Bundle(
        'js/jquery.js',
        'js/bootstrap.min.js',
        'js/slider.js',
        'js/amounts.js',
        'js/landing.js',
        output='js_all.js'
    )
)

env.register(
    'css_all',
    assets.Bundle(
        'css/bootstrap.min.css',
        'css/slider.css',
        'css/font-awesome.min.css',
        'css/landing-page.css',
        output='css_all.css'
    )
)

paypalrestsdk.configure(
  mode="sandbox", # sandbox or live
  client_id=paypal_client_id,
  client_secret= paypal_client_secret
)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/payment/donation/create', methods=["POST"])
def paypal_process():
  amount = 0
  categories = {
    'amount-homeless': 'homeless people',
    'amount-refugees': 'refugees people',
    'amount-orphans': 'orphans people',
    'amount-poverished': 'perverished people'
  }

  items = []

  for key, value in categories.iteritems():
    amount += float(request.form[key])

    if request.form[key] != 0:
      items.append({
        "name": "Donation to " + value,
        "price": "%.2f" % float(request.form[key]),
        "currency": "GBP",
        "quantity": 1
      })

  if amount == 0:
    raise Exception("Invalid amount")

  # Payment
  # A Payment Resource; create one using
  # the above types and intent as 'sale'
  payment = paypalrestsdk.Payment({
    "intent": "sale",

    # Payer
    # A resource representing a Payer that funds a payment
    # Payment Method as 'paypal'
    "payer": {
      "payment_method": "paypal"},

    # Redirect URLs
    "redirect_urls": {
      "return_url": "http://localhost:5000/payment/donation/done",
      "cancel_url": "http://localhost:5000/"},

    # Transaction
    # A transaction defines the contract of a
    # payment - what is the payment for and who
    # is fulfilling it.
    "transactions": [{
      # ItemList
      "item_list": {
        "items": items
      },

      # Amount
      # Let's you specify a payment amount.
      "amount": {
        "total": "%.2f" % amount,
        "currency": "GBP"
      },
      "description": "Donation to Railaid"
    }]
  })
  print(payment)
  # Create Payment and return status
  if payment.create():
    print("Payment[%s] created successfully" % (payment.id))
    # Redirect the user to given approval url
    for link in payment.links:
      if link.method == "REDIRECT":
        # Convert to str to avoid google appengine unicode issue
        # https://github.com/paypal/rest-api-sdk-python/pull/58
        redirect_url = str(link.href)
        return redirect(redirect_url)

  else:
    print(payment.error)

@app.route('/payment/donation/done')
def paypal_success():
  # Don't know what to do with it for now
  payment_id = request.args.get('paymentId')
  payment = paypalrestsdk.Payment.find(payment_id)

  print(payment.transactions[0].amount.total);

  return "Thank you for your donation of " + payment.transactions[0].amount.total + "!"

if __name__ == '__main__':
  app.run(debug=True)

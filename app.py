#!/usr/bin/python
from flask import Flask, session, render_template, url_for, redirect, request, flash, g
from flask.ext import assets
from silver import *
from silver.silverraw import silvershop, silvercom, silverbook, silvercore
import pyxb
import json
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
        'js/moment-with-locales.min.js',
        'js/bootstrap-datetimepicker.min.js',
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
        'css/bootstrap-datetimepicker.min.css',
        'css/slider.css',
        'css/landing-page.css',
        output='css_all.css'
    )
)

# Paypal lib
paypalrestsdk.configure(
  mode="sandbox", # sandbox or live
  client_id=paypal_client_id,
  client_secret= paypal_client_secret
)

# silvercore api
cert = "keys/hacktrain.nokey.pem"
key =  "keys/hacktrain.key"
sc = SilverCore("HackTrain", "GB", "CH2", cert, key)

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

@app.route('/search/tickets')
def search_tickets():
  p1 = Passenger(age=30)

  tp1 = TravelPoint(
      origin="GBQQU",
      destination="GBQQM",
      departure=datetime(2015, 11, 23, 8))

  fq = FareSearch(
          travel_points = [tp1],
          fare_filter = FARE_FILTER.CHEAPEST,
          passengers = [p1])

  fares_result = sc.search_fare(fq)
  fr = fares_result.results
  print(fr)
  return render_template('search-result.html', data=fr)

if __name__ == '__main__':
  app.run(debug=True)

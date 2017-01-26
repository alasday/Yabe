import paypalrestsdk
from flask import request
import urlparse
import dbmanager

paypalrestsdk.configure({
	"mode": "sandbox",
	"client_id": "no_id_for_you",
	"client_secret": "no_secret_for_you"
})
	
def create_payment_for_buyer(item_id):
	item = dbmanager.get_post(item_id)
        price = dbmanager.lowest_bid(item_id)
	
	payment = paypalrestsdk.Payment({
		"intent":"sale",
		"payer": {
			"payment_method":"paypal"
		},
		"redirect_urls": {
			"return_url":"http://127.0.0.1:5000/paid",
			"cancel_url":"http://127.0.0.1:5000/unpaid"
		},
		"transactions": [{
			"item_list": {
				"items": [{
					"name": item["title"],
					"price": price,
					"currency": "USD",
					"quantity": 1
				}]
			},
			"amount": {
				"total": price,
				"currency": "USD"
			},
			"description": ""
		}]
	})
	
	if payment.create():
		print "Payment[%s] created successfully" % (payment.id)
		for link in payment.links:
			if link.method == "REDIRECT":
				redirect_url = str(link.href)
				return redirect_url
	else:
		return "Error while creating payment:"+payment.error

def execute_payment_for_buyer():
	parsed = urlparse.urlparse(request.url)
	query = parsed[4]
	query_parsed = urlparse.parse_qs(query)
	payment_id = query_parsed["paymentId"]
	payer_id = query_parsed["PayerID"]
	payment = paypalrestsdk.Payment.find(payment_id[0])
	if payment.execute({"payer_id": payer_id[0]}):
		return True
	else:
                print payment.error
		return False 
	
#EXAMPLE/TEST
#create_payment_for_buyer(0)

import paypalrestsdk
from flask import request
import urlparse
#import utils

paypalrestsdk.configure({
	"mode": "sandbox",
	"client_id": "no_id_for_you",
	"client_secret": "no_secret_for_you"
})
	
def create_payment_for_buyer(item_id):
	#item = utils.dbmanager.get_item(item_id)
	item = {"name":"test", "price":"5.00", "desc":"test_item"}
	
	payment = paypalrestsdk.Payment({
		"intent":"sale",
		"payer": {
			"payment_method":"paypal"
		},
		"redirect_urls": {
			"return_url":"http://127.0.0.1:5000/buyexec",
			"cancel_url":"http://127.0.0.1:5000/buytest"
		},
		"transactions": [{
			"item_list": {
				"items": [{
					"name": item["name"],
					"price": item["price"],
					"currency": "USD",
					"quantity": 1
				}]
			},
			"amount": {
				"total": item["price"],
				"currency": "USD"
			},
			"description": item["desc"]
		}]
	})
	
	if payment.create():
		print "Payment[%s] created successfully" % (payment.id)
		for link in payment.links:
			if link.method == "REDIRECT":
				redirect_url = str(link.href)
				return "Redirect for approval: %s" % (redirect_url)
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
		return "Payment execute successfully"
	else:
		return payment.error 
	
#EXAMPLE/TEST
#create_payment_for_buyer(0)

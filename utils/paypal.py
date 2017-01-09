import paypalrestsdk
from flask import request
import urlparse
#import utils

paypalrestsdk.configure({
	"mode": "sandbox",
	"client_id": "AQSIxUH2ndmMMKY6dUDu8BSbWZ9v77R7PGbW2zDxzluD3DL5mI6YBA2LZVrBtqgGE331-ZLx1PJPqKXc",
	"client_secret": "ECzSK7bvA-M9_6vDuQaS7QHQpnW3WRWHQxxsewNPQ326ZhCsCjmoygbYkalhmx_WX9mcpnON_GSnFlpI"
})
	
def create_payment_for_buyer(item_id):
	#item = utils.dbmanager.get_item(item_id)
	item = {"name":"test", "price":"5.00", "desc":"test_item"}
	payload = {
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
	}
	
	payment = paypalrestsdk.Payment(payload)
	
	if payment.create():
		print "Payment[%s] created successfully" % (payment.id)
		for link in payment.links:
			if link.method == "REDIRECT":
				redirect_url = str(link.href)
				return "Redirect for approval: %s" % (redirect_url)
	else:
		return "Error while creating payment:"+payment.error

def execute_payment_for_buyer():
	parsed = urlparse.urlparse(request.path)
	print "parsed: ",parsed
	query = parsed[4]
	print "query: ",query
	query_parsed = urlparse.parse_qs(query)
	print "query_parsed: ",query_parsed
	payment_id = query_parsed["paymentId"]
	payer_id = query_parsed["PayerID"]
	payment = paypalrestsdk.Payment.find(payment_id)
	if payment.execute({"payer_id": payer_id}):
		return "Payment execute successfully"
	else:
		return payment.error 
	
#EXAMPLE/TEST
#create_payment_for_buyer(0)
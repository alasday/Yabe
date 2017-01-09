import paypalrestsdk
import os
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
			"return_url":"http://www.sandbox.paypal.com/",
			"cancel_url":"http://www.paypal.com/"
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
		print("Payment[%s] created successfully" % (payment.id))
		for link in payment.links:
			if link.method == "REDIRECT":
				redirect_url = str(link.href)
				print("Redirect for approval: %s" % (redirect_url))
		url = os.environ["REQUEST_URI"] 
		parsed = urlparse.urlparse(url)
		payer_id = parsed["PayerID"]
		if payment.execute({"payer_id": payer_id}):
  			print("Payment execute successfully")
		else:
  			print(payment.error)
	else:
		print("Error while creating payment:")
		print(payment.error)

	
#EXAMPLE/TEST
create_payment_for_buyer(0)
import requests
import base64

client_id="AQSIxUH2ndmMMKY6dUDu8BSbWZ9v77R7PGbW2zDxzluD3DL5mI6YBA2LZVrBtqgGE331-ZLx1PJPqKXc"
client_secret="ECzSK7bvA-M9_6vDuQaS7QHQpnW3WRWHQxxsewNPQ326ZhCsCjmoygbYkalhmx_WX9mcpnON_GSnFlpI"

credentials = "%s:%s" % (client_id, client_secret)
encode_credential = base64.b64encode(credentials)

class Seller:
	email = ""
	fname = ""
	lname = ""
	business_name = ""
	phone = []
	address = []
	item_info = []
	note = ""
	
	#all of the following keys MUST be strings, even if they are numbers
	#phone is a dictionary that contains two keys:
		#"country_code" - should always be "001", this site is US only for now
		#"national_number" - 10 digit phone number
	#address is a dictionary that contains six keys:
		#"line1" - address line 1 (street number)
		#"line2" - address line 2 (apt/suite number) - empty string if none
		#"city" - city
		#"state" - state
		#"postal_code" - zip code
		#"country_code" - always "US"
	#item_info is a list with only one dictionary inside that contains three keys:
		#"name" - item name
		#"quantity" - number of items (most of the time this will be "1")
		#"unit_price" - dictionary that contains two keys:
			#"currency" - always "USD"
			#"value" - price in dollars
	#email, fname, lname, business_name, and note (use get_note() for this) will be strings
	def __init__(self, email, fname, lname, business_name, phone, address, item_info, note):
		self.email = email
		self.fname = fname
		self.lname = lname
		self.business_name = business_name
		self.phone = phone
		self.address = address
		self.item_info = item_info
		self.note = note

class Buyer:
	billing_info = []
	fname = ""
	lname = ""
	business_name = ""
	phone = []
	address = []

def get_token():
	headers = {
		"Authorization": ("Basic %s" % encode_credential),
		'Accept': 'application/json',
		'Accept-Language': 'en_US',
	}

	param = {
		'grant_type': 'client_credentials',
	}

	token = requests.post("https://api.sandbox.paypal.com/v1/oauth2/token", headers=headers, data=param)

	return token["access_token"]
	
def create_invoice(seller_obj, buyer_obj, item_obj access_token):
	headers = {
    	'Content-Type': 'application/json',
    	'Authorization': 'Bearer %s' % access_token,
	}

	data = {
		"merchant_info": {
			"email": seller_obj.email,
			"first_name": seller_obj.fname,
			"last_name": seller_obj.lname,
  			"business_name": seller_obj.business_name,
  			"phone": seller_obj.phone,
  			"address": seller_obj.address
  		},
  		"billing_info": buyer_obj.billing_info
  		"items": seller_obj.item_info,
  		"note": seller_obj.item_note,
  		"payment_term": {"term_type": "NET_45"},
  		"shipping_info": {
  			"first_name": buyer_obj.fname,
  			"last_name": buyer_obj.lname,
  			"business_name": buyer_obj.business_name,
  			"phone": buyer_obj.phone,
			"address": buyer_obj.address
		}
	}
	
	result = requests.post('https://api.sandbox.paypal.com/v1/invoicing/invoices/', headers=headers, data=data)
	print result
	

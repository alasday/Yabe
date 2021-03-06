import paypalrestsdk
from flask import request
import urlparse
import dbmanager
import random
import string
import smtplib

#sends an email from the no-reply account
def send_mail(subject, body, email):
	smtpObj = smtplib.SMTP("smtp.gmail.com",587)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login('yabeapplication@gmail.com',get_keys("email_pw"))
	smtpObj.sendmail('yabeapplication@gmail.com',email,'Subject: %s\n%s'%(subject,body))

def get_keys(string):
        f = open("keys.txt","r")
        lineNum = 0
        for line in f:
                if lineNum == 0 and string == "c_id":
                        return line[:-1]
                if lineNum == 1 and string == "c_sec":
                        return line[:-1]
                if lineNum == 2 and string == "email_pw":
                        return line[:-1]
                lineNum+=1

paypalrestsdk.configure({
	"mode": "sandbox",
	"client_id": get_keys("c_id"),
	"client_secret": get_keys("c_sec")
})

def create_payment_for_buyer(item_id):
	item = dbmanager.get_post(item_id)
        price = dbmanager.lowest_bid(item_id)["price"]
	
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
		print payment.error
                return "Error"

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

def create_payment_to_seller(email,item_id):
	item = dbmanager.get_post(item_id)
        price = dbmanager.lowest_bid(item_id)["price"]
        
	payout = paypalrestsdk.Payout({
                "sender_batch_header": {
                        "sender_batch_id": sender_batch_id,
                        "email_subject": "You have a payment"
                },
                "items": [
                        {
                                "recipient_type": "EMAIL",
                                "amount": {
                                        "value": int(price*0.95), #account for fees
                                        "currency": "USD"
                                },
                                "receiver": email,
                                "note": "Payout for Yabe item!",
                                "sender_item_id": str(item_id)
                        }
                ]
        })
	
	if payout.create():
                print("payout[%s] created successfully" %(payout.batch_header.payout_batch_id))
	else:
		print payout.error
                return "Error"

sender_batch_id = ''.join(
    random.choice(string.ascii_uppercase) for i in range(12))


#EXAMPLE/TEST
#create_payment_for_buyer(0)

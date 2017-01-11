from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from utils import paypal
from  utils import dbmanager 
import urllib2, json

app = Flask(__name__)
#f = open( "utils/key", 'r' )
app.secret_key = "hello"#f.read();
#f.close()

#root, two behaviors:
#    if logged in: redirects you to your feed
#    if not logged in: displays log in/register page
@app.route("/")
def loginOrRegister():
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    else:
        return render_template("index.html")

@app.route("/register")
def register():
	return render_template("register.html")
	
@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/pay")
def pay():
	#item = dbmanager.get_item(item_id)
	item = {"name":"test", "price":"5.00", "desc":"test_item"}
	link = paypal.create_payment_for_buyer(0)
	return render_template("pay.html",link = link)

#handles the feed
#@app.route("/feed)
#def feed():
	#how dowe wantto organize this (most popular? most recent at top?) 
	#return render_template("feed.html,link=link)

#handles input of the login register page
@app.route("/authOrCreate", methods=["POST"])
def authOrCreate():
    formDict = request.form
    print formDict
    if formDict["logOrReg"] == "login":
        username = formDict["username"]
        password = formDict["password"]
        loginStatus = "login failed"
        statusNum = accountManager.authenticate(username,password) #returns 0,1 or 2 for login status messate
        if statusNum == 0:
            loginStatus = "user does not exist"
        elif statusNum == 1:
            session["username"]=username
            loginStatus = username + " logged in"
            return redirect( "/profile" )
        elif statusNum == 2:
            loginStatus = "wrong password"

        return render_template("loginOrReg.html",status=loginStatus)

    elif formDict["logOrReg"] == "register":  #registering
        username = formDict["username"]
        password = formDict["password"]
        pwd = formDict["passconfirm"]  #confirm password
        registerStatus = "register failed"
        statusNum = accountManager.register(username,password,pwd) #returns true or false
        if statusNum == 0:
            registerStatus = "username taken"
        elif statusNum == 1:
            registerStatus = "passwords do not match"
        elif statusNum == 2:
            registerStatus = username +" account created"

        return render_template("loginOrReg.html",status=registerStatus) #status is the login/creation messate 
    else:
        return redirect(url_for("loginOrReg"))

#logout of user
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop('username')
        return render_template("loginOrReg.html",status="logged out") 
    else:
        return redirect(url_for('loginOrRegister'))

#test route for buying (noah)
@app.route('/buytest', methods=["POST", "GET"])
def buytest():
	print paypal.create_payment_for_buyer(0)
        return "check console"
	
@app.route('/buyexec', methods=["POST", "GET"])
def buyexec():
	print paypal.execute_payment_for_buyer()
        return "check paypal"
    
if __name__ == "__main__":
    app.debug = True
    app.run()

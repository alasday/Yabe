#imports
from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from utils import paypal
from utils import dbmanager
from utils import accountManager
import urllib2, json

#create a flask app (secret key created when initialize.py is run)
app = Flask(__name__)
f = open( "utils/key", 'r' )
app.secret_key = "hello"#f.read();
f.close()

#the default page is allows you to choose to login or register
@app.route("/")
def loginOrRegister():
	if 'username' in session:
	    return render_template("index.html",username = session['username'])
	else:
		return render_template("index.html")

#register page if you don't already have an account
@app.route("/register")
def register():
	return render_template("register.html")

#login page if you already have an account
@app.route("/login")
def login():
	return render_template("login.html")

#payment page (you have to be logged in to pay for something)
@app.route("/pay")
def pay():
	#item = dbmanager.get_item(item_id)
	item = {"name":"test", "price":"5.00", "desc":"test_item"}
	link = paypal.create_payment_for_buyer(0)
	return render_template("pay.html",link = link)

#handles input of the login register page
#authenticates/creates accounts
@app.route("/authOrCreate", methods=["POST"])
def authOrCreate():
    formDict = request.form
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

		#to be changed
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
	    return redirect("/login") #WE NEED TOPUT AT THE TOP OF THE LOGIN PAGE: 'Username successfully registered, please log in'
        return render_template("loginOrReg.html",status=registerStatus) #status is the login/creation messate 
    else:
        return redirect(url_for("loginOrReg"))

#creates a buy request post
@app.route("/create", methods=["POST"])
def create():
        #get field stuff
        new_post(session['username'], request.form["title"], request.form["startingPrice"],request.form["period"])
        return redirect(url_for('/')) #redirect to /feed once we have a feed, we can redirect to the feed once you have made a post

#creates the feed of buy request posts
@app.route("/feed", methods=["GET", "POST"])
def feed():
    if request.method == "POST":
        # Add contribution to the database
        post_id = request.form["post_id"]
        return render_template("buy.html")
    else:
        # View all posts
        posts = []
        return render_template("feed.html")

#form for item info
@app.route("/buy")
def buy():
	if 'username' in session:
		return render_template("buy.html")
	else:
		return redirect(url_for('loginOrRegister'))

#form for profile, show specific profile info
@app.route("/profile", methods=["POST", "GET"])
def profile():
	if request.form:
		accountManager.set_user_info(session['username'], request.form.get("email"), request.form.get("addr1"), request.form.get("addr2"), request.form.get("city"), request.form.get("state"), request.form.get("zip"), request.form.get("fname"), request.form.get("lname"), request.form.get("phone"))
	if 'username' in session:
		return render_template("profile.html",user_info = accountManager.get_user(session['username']), filled_out = accountManager.full_user_info(session['username']))
	else:
		return redirect(url_for('loginOrRegister'))

#logout of user
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop('username')
        render_template("loginOrReg.html",status="logged out")
        return redirect("/login")
    else:
        return redirect(url_for('loginOrRegister'))

#test route for buying (noah)
@app.route('/buytest', methods=["POST", "GET"])
def buytest():
	print paypal.create_payment_for_buyer(0)
        return "check console"

#execute the paypal payment
@app.route('/buyexec', methods=["POST", "GET"])
def buyexec():
	print paypal.execute_payment_for_buyer()
        return "check paypal"

#run the app
if __name__ == "__main__":
    app.debug = True
    app.run()

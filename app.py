from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from utils import paypal
from utils import dbmanager
from utils import accountManager
import urllib2, json
  
app = Flask(__name__)
f = open( "utils/key", 'r' )
app.secret_key = "hello"#f.read();
f.close()

@app.route("/")
def loginOrRegister():
	if 'username' in session:
	    return render_template("index.html",username = session['username'])
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
#NOTE: the homepage will be the feed! You can see what other people have requested/offered but cannot request to offer anything yourself UNTIL you log in
@app.route("/feed") 
def feed():
	return render_template("feed.html")

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

#@app.route("/create", methods=["GET", "POST"])
#def create():
#    # Create new post
#    pass
#
#@app.route("/contribute", methods=["GET", "POST"])
#def contribute():
#    if request.method == "POST":
#        # Add contribution to the database
#        post_id = request.form["post_id"]
#        return render_template("buy.html")
#    else:
#        # View all posts
#        posts = []
#        return render_template("buy.html", stories=stories)

#form for item info
@app.route("/buy")
def buy():
	if 'username' in session:
        #Do we not need a form on buy.html where you input the title, startingPrice, and period? Because then we need to call new_post and put all those in:
#               new_post(session['username'], request.form["title"], request.form["startingPrice"],request.form["period"])
		return render_template("buy.html")
	else:
		return redirect(url_for('loginOrRegister'))

#form for profile, show specific profile info
@app.route("/profile")
def profile():
	if 'username' in session:
		return render_template("profile.html",user_info = dbmanager.get_user(session['username']), filled_out = False)
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
	
@app.route('/buyexec', methods=["POST", "GET"])
def buyexec():
	print paypal.execute_payment_for_buyer()
        return "check paypal"
    
if __name__ == "__main__":
    app.debug = True
    app.run()

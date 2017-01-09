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
        return render_template("index.html", images=images, tagStrings=tagStrings, username=session['username'])
    else:
        return render_template("index.html", images=images, tagStrings=tagStrings)

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
        pwd = formDict["pwd"]  #confirm password
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
	return paypal.create_payment_for_buyer(0)
	
@app.route('/buyexec', methods=["POST", "GET"])
def buyexec():
	return paypal.execute_payment_for_buyer()
    
if __name__ == "__main__":
    app.debug = True
    app.run()
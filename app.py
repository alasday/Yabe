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

@app.route("/unpaid")
def unpaid():
    if not "status" in session:
        return redirect("/feed")
    sale_link = paypal.create_payment_for_buyer(int(session["status"]))
    return render_template("unpaid.html",sale_link = sale_link)

@app.route("/paid")
def paid():
    if paypal.execute_payment_for_buyer():
        postId = int(session["status"])
        lowest_bid = dbmanager.lowest_bid(postId)
        dbmanager.log_sale(postId,lowest_bid["id"])
        email = accountManager.get_user(lowest_bid["bidder"])["email"]
        print email
        payout_link = paypal.create_payment_to_seller(email,postId)
        session.pop("status")
        return redirect("/feed")
    return render_template("unpaid.html")
    
@app.route("/enditem/<int:postId>")
def enditem(postId=None):
    dbmanager.end_post(postId)
    return redirect("/unpaid")
    
#register page if you don't already have an account
@app.route("/register")
def register():
    if "status" in session:
        return redirect("/unpaid")
    return render_template("register.html")

#login page if you already have an account
@app.route("/login")
def login():
    print session
    if "status" in session:
        return redirect("/unpaid")
    return render_template("login.html")

#handles input of the login register page
#authenticates/creates accounts
@app.route("/authOrCreate", methods=["POST"])
def authOrCreate():
    if "status" in session:
        return redirect("/unpaid")
    formDict = request.form
    if formDict["logOrReg"] == "Login":
        username = formDict["username"]
        password = formDict["password"]
        loginStatus = "login failed"
        statusNum = accountManager.authenticate(username,password) #returns 0,1 or 2 for login status messate
        print statusNum
        if statusNum == 0:
            loginStatus = "user does not exist"
        elif statusNum == 1:
            session["username"]=username
            loginStatus = username + " logged in"
            return redirect( "/feed")
        elif statusNum == 2:
            loginStatus = "wrong password"
        else:
            session["username"] = username
            if statusNum == -1:
                statusNum = 0
            if statusNum == -2:
                statusNum = 1
            if statusNum == -3:
                statusNum = 2
            session["status"] = statusNum
            return redirect("/feed")

                #to be changed
        return render_template("loginOrReg.html",status=loginStatus)

    elif formDict["logOrReg"] == "Register":  #registering
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
        return redirect(url_for("loginOrRegister"))
    
#creates a buy request post
@app.route("/create", methods=["POST"])
def create():
    if "status" in session:
        return redirect("/unpaid")
        #get field stuff
    pId = dbmanager.new_post(session['username'], request.form["title"], int(request.form["startingPrice"]),int(request.form["period"]))
    #return redirect('/post/<int: postId>')
    return redirect(url_for('post',postId = pId))

#actually posts the buy request post
@app.route('/post/<int:postId>',methods=["POST","GET"])
def post(postId=None):
    if "status" in session:
        return redirect("/unpaid")
    if "Submit" in request.form:
        dbmanager.new_bid(session['username'],postId,int(request.form.get("amt")))
    bids = dbmanager.get_bids(postId)
    startingPrice = dbmanager.get_post(postId)['startingPrice']
    lowestBid = startingPrice
    lowestBidId = -1
    for i in bids:
        if int(i["price"]) < lowestBid:
            lowestBid = int(i["price"])
            lowestBidId = i["id"]
    return render_template("post.html", username = session['username'], post = dbmanager.get_post(postId), lowestBidId = lowestBidId, lowestBidInfo = dbmanager.get_bid(lowestBidId), allBids = bids)
    
@app.route("/bid/<int:postId>", methods=["POST","GET"])
def bid(postId=None):
    if "status" in session:
        return redirect("/unpaid")
    bids = dbmanager.get_bids(postId)
    startingPrice = dbmanager.get_post(postId)['startingPrice']
    lowestBid = startingPrice
    lowestBidId = -1
    for i in bids:
        if int(i["price"]) < lowestBid:
            lowestBid = int(i["price"])
            lowestBidId = i["id"]
    return render_template("bid.html", postId = postId, username = dbmanager.get_post(postId)["owner"], startingPrice = startingPrice, lowestBidId = lowestBidId, lowestBidInfo = dbmanager.get_bid(lowestBidId), allBids = bids)

#creates the feed of buy request posts
@app.route("/feed", methods=["GET", "POST"])
def feed():
    dbmanager.update_posts()
    if "status" in session:
        return redirect("/unpaid")
    if request.method == "POST":
        # Add contribution to the database
        post_id = request.form["post_id"]
        return render_template("buy.html")
    else:
        # View all posts
        if "username" in session:
            username = session["username"]
        else:
            username = ""
        posts = []
        num = -1
        if "status" in session:
            num = session["status"]
                
    return render_template("feed.html",username=username,posts=dbmanager.get_posts(100),num = num)

#creates the feed of buy request posts made by a certain
#@app.route("/feed")
#@app.route("/feed/<string: username>/", methods=["GET", "POST"])
@app.route("/user/<username>/")
def userposts(username):
    if "status" in session:
        return redirect("/unpaid")
    #view all posts by username
    posts = []
    return render_template("user.html",username=username,posts=dbmanager.get_posts_by_username(username))

#ajax code by mr brown just to show how ajax is done
#bc i didnt totally get the way to do it and its a
#lot simpler than the other thing i linked... not
#entirely sure how to do it but we can try and bounce
#ideas off each other
#from flask import Flask,request,url_for,redirect,render_template
#import time
#import json
#
#
#app=Flask(__name__)
#
#@app.route("/")
#def index():
#    return render_template("index.html")
#
#@app.route("/upcase")
#def upcase():
#    data = request.args.get("text")
#    print data
#    
#    time.sleep(5)
#    
#    result = {'original':data,
#              'result':data.upper()
#    }
#    
#    return json.dumps(result)

#THIS IS A WAY I FOUND (http://flask.pocoo.org/snippets/10/) THAT ALLOWS US TO INCORPORATE AJAX INTO THE FEED
#from urlparse import urljoin
#from flask import request
#from werkzeug.contrib.atom import AtomFeed
#def make_external(url):
#    return urljoin(request.url_root, url)
#@app.route('/recent.atom')
#def recent_feed():
#    feed = AtomFeed('Recent Articles',
#                    feed_url=request.url, url=request.url_root)
#    articles = Article.query.order_by(Article.pub_date.desc()) \
#                      .limit(15).all()
#    for article in articles:
#        feed.add(article.title, unicode(article.rendered_text),
#                 content_type='html',
#                 author=article.author.name,
#                 url=make_external(article.url),
#                 updated=article.last_update,
#                 published=article.published)
#    return feed.get_response()

#psuedo-code for how this would work
#def handle_request(request):
#    data = get_more_data(request)
#    return send_response(data)
#
#def handle_request(request):
#    # If there's no data available, greenlet will sleep
#    # and execution will be transferred to another greenlet
#    data = get_more_data(request)
#    return make_response(data)
#
#def handle_request(request):
#    get_more_data(request, callback=on_data)
#
#def on_data(request):
#    send_response(request, make_response(data))
#
#@coroutine
#def handle_request(request):
#    data = yield get_more_data(request)
#    return make_response(data)
#@coroutine
#def get_mode_data(request):
#    data = yield make_db_query(request.user_id)
#    return data
#
#def process_request(request):
#    data = get_more_data(request)
#    return data

#ACTUALLY THISLOOKS LIKE IT'S THE BEST DEMO OF A DYNAMIC FEED USINGPYTHON/AJAX: http://www.giantflyingsaucer.com/blog/?p=4310
    
#form for item info
@app.route("/buy")
def buy():
    if "status" in session:
        return redirect("/unpaid")
    if 'username' in session:
        return render_template("buy.html", username=session["username"])
    else:
        return redirect(url_for('loginOrRegister'))

#form for profile, show specific profile info
@app.route("/profile", methods=["POST", "GET"])
def profile():
    if "status" in session:
        return redirect("/unpaid")
    if request.form and not accountManager.full_user_info(session['username']):
        accountManager.set_user_info(session['username'], request.form.get("email"), request.form.get("addr1"), request.form.get("addr2"), request.form.get("city"), request.form.get("state"), request.form.get("zip"), request.form.get("fname"), request.form.get("lname"), request.form.get("phone"))
    if 'username' in session:
        return render_template("profile.html",user_info = accountManager.get_user(session['username']), filled_out = accountManager.full_user_info(session['username']), username=session["username"])
    else:
        return redirect(url_for('loginOrRegister'))

#when updating user info
@app.route("/profileupdate", methods=["POST"])
def profileupdate():
    if "status" in session:
        return redirect("/unpaid")
    if 'username' in session and request.form:
        user_info = accountManager.get_user(session['username'])
        if request.form.get("inputChangeNameF") == '':
            nameF = user_info["nameF"]
        else:
            nameF = request.form.get("inputChangeNameF")
            
        if request.form.get("inputChangeNameL") == '':
            nameL = user_info["nameL"]
        else:
            nameL = request.form.get("inputChangeNameL")
            
        if request.form.get("inputChangeEmail") == '':
            email = user_info["email"]
        else:
            email = request.form.get("inputChangeEmail")
                
        if request.form.get("inputChangeAddr1") == '':
            addr1 = user_info["addr1"]
        else:
            addr1 = request.form.get("inputChangeAddr1")
                        
        if request.form.get("inputChangeAddr2") == '':
            addr2 = user_info["addr2"]
        else:
            addr2 = request.form.get("inputChangeAddr2")
                        
        if request.form.get("inputChangeCity") == '':
            city = user_info["addrCity"]
        else:
            city = request.form.get("inputChangeCity")
                        
        if request.form.get("inputChangeState") == '':
            state = user_info["addrState"]
        else:
            state = request.form.get("inputChangeState")
                        
        if request.form.get("inputChangeZip") == '':
            zip = user_info["addrZip"]
        else:
            zip = request.form.get("inputChangeZip")
                
        if request.form.get("inputChangePhone") == '':
            phone = user_info["phone"]
        else:
            phone = request.form.get("inputChangePhone")
            accountManager.set_user_info(session["username"], email, addr1, addr2, city, state, zip, nameF, nameL, phone)
    return redirect("/profile")

#logout of user
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "status" in session:
        return redirect("/unpaid")
    if "username" in session:
        session.pop('username')
        return redirect("/login")
    else:
        return redirect(url_for('loginOrRegister'))

#run the app
if __name__ == "__main__":
    app.debug = True
    app.run()

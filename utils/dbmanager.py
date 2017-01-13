import sqlite3, time

def get_user( username ):
    ret = {}
    
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    checkUser = 'SELECT *  FROM users WHERE username == "%s";' % ( username )  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone()

    ret["email"] = l[3]
    ret["addr1"] = l[4]
    ret["addr2"] = l[5]
    ret["addrCity"] = l[6]
    ret["addrState"] = l[7]
    ret["addrZip"] = l[8]
    ret["nameF"] = l[9]
    ret["nameL"] = l[10]
    ret["phone"] = l[11]
    
    return ret

#testing get_user
#print get_user("jack")

# new_post() -- method for creating a new post
def new_post( owner, title, startingPrice, period ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    # finding the next postId
    q = "SELECT postId FROM posts"
    c.execute(q)

    IDS = c.fetchall()

    if IDS: # if list is not empty, there exists ids to take the max of
        postId = max(IDS)[0] + 1
    else: 
        postId = 0 #first post

    date = time.time()

    secondsPerDay = 86400
    expires = date + secondsPerDay * period
    
    q = """
    INSERT INTO posts VALUES('%s', '%d', '%s', '%d', '%f', '%f');
    """ % ( owner, postId, title, startingPrice, date, expires )

    c.execute( q )

    db.commit()
    db.close()

#testing new_post
#new_post("jim", "im lit ", 12, 12)


# returns a dict in the form:
# dict = {
#  "title" : title,
#  "startingPrice" : startingPrice
# }
# I can add more stuff if anyone needs it
def get_post( postId ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    q = "SELECT * FROM posts WHERE postId  = '%s';" % ( postId )
    c.execute( q )

    lit = c.fetchall()

    dict = {}
    dict["title"] = lit[0][2]
    dict["startingPrice"] = lit[0][3]
    dict['postId'] = lit[0][1]
    
    db.commit()
    db.close()

    return dict

#testing get_post
#print get_post( 0 )

# new_bid()
# adds a bid to a given item
def new_bid( bidder, postId, price ):
    status = 0 # success
    
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    #find the next bidId
    q = "SELECT bidId FROM bids;"
    c.execute(q)

    IDS = c.fetchall()

    if IDS: # if list is not empty, there exists ids to take the max of
        bidId = max(IDS)[0] + 1
    else:    
        bidId = 0 #the first bid
    
    date = time.time()

    q = "SELECT price FROM bids WHERE postId = '%d';" % ( postId )
    c.execute(q)

    bidPricesL = c.fetchall()

    if bidPricesL: #if the list is not empty, there have been bids on this post
        minBid = min( bidPricesL )[0]

        if price >= minBid:
            #print "price bid higher than last bid, returning 1"
            return 1 # price bid is higher than lowest current bid

    else: #no bids have been made on this item
         q = "SELECT startingPrice FROM posts WHERE postId = '%d';" % ( postId )
         c.execute(q)
         
         startingPrice = c.fetchone()[0]
         if price >= startingPrice:
             #print "price bid higher than starting price, returning 1"
             return 1;
    
    # at this point, a bid must have an lower price than the last bid (or startingPrice if no bids yet)
    q = """
    INSERT INTO bids VALUES('%s', '%d', '%d', '%d', '%f');
    """ % ( bidder, postId, bidId, price, date )

    c.execute( q )

    db.commit()
    db.close()

    return status

#testing new_bid
#new_bid( "jack", 4, 11 ) 

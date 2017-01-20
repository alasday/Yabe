import sqlite3, time


# new_post() -- method for creating a new post
# @returns postId
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
    
    return postId

    
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

    lit = c.fetchone()

    dict = {}
    dict['owner'] = lit[0]
    dict['postId'] = lit[1]
    dict["title"] = lit[2]
    dict["startingPrice"] = lit[3]

    expires = lit[5]
    currentDate = time.time()
    periodSeconds = expires - currentDate
    secondsPerDay = 86400
    secondsPerHour = 3600
    
    if periodSeconds < 0:
        period = "This listing has expired"
    else:
        if periodSeconds / secondsPerDay > 2:
            period = str(int(periodSeconds / secondsPerDay)) + " days"
        else:
            period = str(int(periodSeconds / secondsPerHour)) + " hours"

    dict['period'] = period        

    
    
    db.commit()
    db.close()

    return dict

#testing get_post
#print get_post( 0 )

def get_posts( number ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    now = time.time()
    
    q = "SELECT postId FROM posts WHERE expires > %d;" % ( now )
    c.execute( q )
    
    ids = c.fetchall()
    
    start = len(ids) - number
    if start > 0:
        ret = [None] * (number)
        for i in range( start, len(ids) ):
            ret[number - (i - start + 1)] =  get_post( ids[i][0] )
    else:
        ret = [None] * len(ids)
        for i in range( len(ids) ):
            ret[len(ids) - (i + 1)] = get_post( ids[i][0] ) 
                  
    return ret

#testing get_posts
#print get_posts(5)

def get_posts_by_username( username ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    now = time.time()
    
    q = "SELECT postId FROM posts WHERE owner = '%s'  ;" % ( username )
    c.execute( q )
    
    ids = c.fetchall()

    ret = [None] * len(ids)
    for i in range( len(ids) ):
        ret[len(ids) - (i + 1)] = get_post( ids[i][0] ) 
              
    return ret

#testing get_posts_by_username
#print get_posts_by_username('jim')



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
    
        startingPrice = c.fetchall()[0]
        #print "startingPrice: ", startingPrice
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
#new_bid( "jack", 4, 9 ) 

def get_bid( bidId ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    q = "SELECT * FROM bids WHERE bidId = %d  ;" % ( bidId )
    c.execute( q )
    
    bids = c.fetchone()
    # print "bids: ", bids
    
    if bids == None:
    	return None

    ret = {}
    ret['bidder'] = bids[0]
    ret['id'] = bids[2]
    ret['price'] = bids[3]
    ret['date'] = bids[4]
    return ret

#testing get_bit
#print get_bid(0)

def get_bids( postId ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    q = "SELECT bidId FROM bids WHERE postId = %d ;" % ( postId  )
    c.execute( q )
    
    ids = c.fetchall()
    
    ret = [None] * len(ids)
    for i in range( len(ids) ):
        ret[len(ids) - (i + 1)] = get_bid( ids[i][0] ) 
                  
    return ret

#testing get_bids
#print get_bids(4)

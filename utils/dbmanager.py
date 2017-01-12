import sqlite3, time

def getUserInfo( userId ):
    ret = {}
    
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    checkUser = 'SELECT *  FROM users WHERE userId=="%s";' % ( userId )  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone()

    db.commit()
    db.close()
    print

    return ret
    
    
def get_item(item_id):
	ret = {}
	#need:
		#"name"
		#"price"
		#"desc"

def new_post( owner, title, startingPrice, period ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    q = "SELECT postId FROM posts"
    c.execute(q)

    IDS = c.fetchall()

    if IDS: # if list is not empty, there exists ids to take the max of
        postId = max(IDS)[0] + 1
    else:    
        postId = 0

    date = time.time()

    secondsPerDay = 86400
    expires = date + secondsPerDay * period
    
    q = """
    INSERT INTO posts VALUES('%s', '%d', '%s', '%d', '%f', '%f');
    """ % ( owner, postId, title, startingPrice, date, expires )

    c.execute( q )

    db.commit()
    db.close()

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

    db.commit()
    db.close()

    return dict

#print get_post( 0 )

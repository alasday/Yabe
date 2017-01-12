import sqlite3   #enable control of an sqlite database

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
        postId = max(IDS)
    else:    
        postId = 0

    date = 5
    expires = date + period
    
    q = """
    INSERT INTO posts VALUES('%s', '%d', '%s', '%d', '%d', '%d')
    """ % ( owner, postId, title, startingPrice, date, expires )

    c.execute( q )

    db.commit()
    db.close()

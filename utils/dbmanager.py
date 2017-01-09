import sqlite3   #enable control of an sqlite database

def getUserInfo( userId ):
    ret = {}
    
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    checkUser = 'SELECT *  FROM users WHERE userId=="%s";' % ( userId )  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone()

    print

    return ret
    
    
def get_item(item_id):
	ret = {}
	#need:
		#"name"
		#"price"
		#"desc"
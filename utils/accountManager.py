#Manages the account info tables in the db
import sqlite3   #enable control of an sqlite database

''' 
1. authenticate: authenticate credentials
2. register: make sure username not used
'''

from hashlib import sha1
import dbmanager

def unpaidInvoice(user):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("SELECT * FROM posts WHERE owner='%s' and active='1'" %(user))
    l = c.fetchall()
    if l == None:
        return -1
    else:
        postIds = []
        for row in l:
            postIds.append(row[1])
        for pid in postIds:
            lowest_bid = dbmanager.lowest_bid(int(pid))
            c.execute("SELECT * FROM sales WHERE postId='%s'"%(pid))
            row = c.fetchone()
            if row == None:
                return pid
    return -4

#authenticate user returns true if authentication worked
def authenticate(user,password):

    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok
    isLogin = False #Default to false; login info correct?
    loginStatusMessage = "" #what's wrong
    messageNumber = 0 #represents what kind of error it is
    passHash = sha1(password).hexdigest()#hash it

    checkUser = 'SELECT * FROM users WHERE username=="%s";' % (user)  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone() #listifies the results
    print l
    if l == None:
        isLogin = False
        messageNumber = 0
        loginStatusMessage = "user does not exist"
    elif l[1] == passHash:
        isLogin = True
        messageNumber = 1
        loginStatusMessage = "login info correct"
        if unpaidInvoice(user) != -4:
            messageNumber = unpaidInvoice(user)
            if messageNumber == 0:
                messageNumber = -1
            if messageNumber == 1:
                messageNumber = -2
            if messageNumber == 2:
                messageNumber = -3
    else:
        isLogin = False
        messageNumber = 2
        loginStatusMessage = "wrong password"
        
    db.commit() #save changes
    db.close()  #close database
    return messageNumber

#returns true if register worked
def register(user,password,pwd):    #user-username, password-password, pwd-retype
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok
    isRegister = False #defualt not work
    registerStatus = ""
    messageNumber = 0 #for message


    checkUser = 'SELECT * FROM users WHERE username=="%s";' % (user)  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone() #listifies the results

    if l != None:
        isRegister = False
        messageNumber = 0
        registerStatus = "username taken"
    elif (password != pwd):
        isRegister = False
        messageNumber = 1
        registerStatus = "passwords do not match"
    elif (password == pwd):
        #get latest id
        getLatestId = "SELECT userId FROM users"
        c.execute(getLatestId)
        l = c.fetchall()
        if l: #if list is not empty, there exists ids to take the max of
            userId = max(l)[0]+1
        else: #first user to register
            userId = 0

    	passHash = sha1(password).hexdigest()#hash it
        insertUser = 'INSERT INTO users VALUES ("%s","%s","%s","","","","","","","","","");' % (user,passHash,userId) #sqlite code for inserting new user
        c.execute(insertUser)

        isRegister = True
        messageNumber = 2
        registerStatus = "user %s registered!" % (user)

    db.commit() #save changes
    db.close()  #close database
    return messageNumber

#testing register
#register("jack", "jack", "jack")


#set_user_info
def set_user_info( username, email, addr1, addr2, addrCity, addrState, addrZip, nameF, nameL, phone):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    q = """
    UPDATE users SET email = '%s', addr1 = '%s', addr2 = '%s', addrCity = '%s', addrState = '%s', addrZip = '%s', nameF = '%s', nameL = '%s', phone = '%s' 
    WHERE username = '%s';""" % (email, addr1, addr2, addrCity, addrState, addrZip, nameF, nameL, phone, username)

    c.execute(q)

    db.commit()
    db.close()

set_user_info("jack", "testemail.com", "230 b 142", "11844", "nyc", "NY", "11694", "Jack", "Schluger", "917 391 7995")

def full_user_info( username ):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    checkUser = 'SELECT *  FROM users WHERE username == "%s";' % ( username )  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone()

    for s in l:
        if s == '':
            return False
    return True

#testing full_user_info
#print full_user_info("jack")

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
    ret["user"] = username
    
    return ret

#testing get_user
#print get_user("jack")

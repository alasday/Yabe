#!/usr/bin/python
'''
block comment describing the contents of this file
'''
import sqlite3   #enable control of an sqlite database
import os

keyFile = open("utils/key", "w")
keyFile.write(os.urandom(32))
keyFile.close()

f = "database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#------------------------create tables---------------------------------------
q = "CREATE TABLE users (username TEXT, password TEXT, userId INTEGER, email TEXT , addr1 TEXT, addr2 TEXT, addrCity TEXT, addrState TEXT, addrZip TEXT, nameF TEXT, nameL TEXT, phone TEXT)"
c.execute(q)

q="CREATE TABLE posts (owner TEXT, postId INTEGER, title TEXT, startingPrice INTEGER, date FLOAT, expires FLOAT, active TEXT)"
c.execute(q)

q="CREATE TABLE bids (bidder TEXT, postId INTEGER, bidId INTEGER, price INTEGER, date FLOAT)"
c.execute(q)

q="CREATE TABLE sales (postId INTEGER, bidId INTEGER,  saleId INTEGER, date FLOAT)"
c.execute(q)

db.commit()
db.close()

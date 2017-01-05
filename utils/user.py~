import sqlite3
import hashlib

DATABASE = "database.db"

def get_user(**kwargs):
    if not kwargs:
        return None

    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    criterion = []
    params = []
    for k,v in kwargs.items():
        criterion.append("%s = ?" % k)
        params.append(str(v))

    query = "SELECT * FROM users WHERE %s" % " AND ".join(criterion)
    c.execute(query, params)

    result = c.fetchone()
    db.close()
    return result

def add_user(username, password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    password = hashlib.sha256(password).hexdigest()

    query = "INSERT INTO users VALUES (NULL, ?, ?, '', 0, 0, '', 0)"
    c.execute(query, (username, password,))
    db.commit()
    db.close()

def save_settings(username, settings):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    zip_code = settings['zip_code']

    if "subway" in settings:
        subway = 1
    else:
        subway = 0

    if "bus" in settings:
        bus = 1
        busNum = settings['busNum']
    else:
        bus = 0
        busNum = ''

    if "lirr" in settings:
        lirr = 1;
    else:
        lirr = 0;

    query = "UPDATE users SET zip_code = ?, subway = ?, bus = ?, busNum = ?, lirr = ? WHERE username = ?"

    c.execute(query, (zip_code, subway, bus, busNum, lirr, username))
    db.commit()
    db.close()

def get_settings(username):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    fields = ["zip_code", "subway", "bus", "busNum", "lirr"]
    query = "SELECT %s FROM users WHERE username = '%s'" % (", ".join(fields), username)
    c.execute(query)
    db.commit()
    result = c.fetchone()
    db.close()

    d = {}

    if not result:
        return d

    i = 0
    while (i < len(fields)):
        if result[i]:
            d[fields[i]] = result[i]
        i += 1

    return d;

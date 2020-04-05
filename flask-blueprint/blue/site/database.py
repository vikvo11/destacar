#import os
#from blue import app
#print ('Loading the modules in the blue\site folder...')
#app.config['DATABASE']='Dev.db'
from blue import app
from flask import g
import sqlite3
from passlib.hash import sha256_crypt

#app.config['DATABASE']='blue/site/Dev.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		print(app.config['DATABASE'])
		db = g._database = sqlite3.connect(app.config['DATABASE'])
		db.row_factory = sqlite3.Row
	return db
@app.teardown_appcontext
#@mod.teardown_request
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

#Initial Schemas -
'''
You can then create such a database from the Python shell:
>>> from yourmodlication import init_db
>>> init_db()
'''
def init_db():
	with mod.app_context():
		db = get_db()
		with mod.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

'''
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value)
		for idx, value in enumerate(row))

db.row_factory = make_dicts
'''

def valid_login(username, password):
    user = query_db('select * from users where username = ?',[username], one=True)
    if user is None:
        print(username +" is NONE")
        return False
    else:
        if sha256_crypt.verify(password,user['password']):
            return True
        else:
            return False
def log_the_user_in(username):
    return render_template('profile.html', username=username)

def register_user(name, email, username, password):
    query_db("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",(name, email, username, password))
    get_db().commit()

#import form menu.py >>
#cur.execute("CREATE TABLE IF NOT EXISTS users(name text, email string, username string, password string)")
#cur.execute("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",(name, email, username, password))

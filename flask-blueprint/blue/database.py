#import os
#from blue import app
#print ('Loading the modules in the blue\site folder...')
#app.config['DATABASE']='Dev.db'
from blue import app
from flask import g
#from flask import request,url_for
import sqlite3
#from flask_mysqldb import MySQL #For connect to MySQL DB
from passlib.hash import sha256_crypt
import os

#
from blue.config import ROOT_DIR,file_path
#####sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from sqlalchemy.ext.hybrid import hybrid_property

# Create in-memory database
app.config['DATABASE_FILE'] = 'db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
####

db = SQLAlchemy(app)
####

#Config mysql
#app.config['MYSQL_HOST']='Ladymarlene.mysql.pythonanywhere-services.com'
#app.config['MYSQL_USER']='Ladymarlene'
#app.config['MYSQL_PASSWORD']='cb.,fq12-'
#app.config['MYSQL_DB']='Ladymarlene$bot'
#app.config['MYSQL_CURSORCLASS']='DictCursor'
#init MySQL
#dbm=MySQL(app)

'''
def upd_db():
	for i in [1, 2, 3]:
	    file = File()
	    file.name = "Example " + str(i)
	    file.path = "example_" + str(i) + ".pdf"
	    db.session.add(file)
'''
#app.config['DATABASE']='blue/site/Dev.db'

# Create DB models
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username=db.Column(db.Unicode(64))
	password=db.Column(db.Unicode(128))
	#password = db.Column(db.Binary)


	first_name = db.Column(db.Unicode(64))
	last_name = db.Column(db.Unicode(64))
	email = db.Column(db.Unicode(128))
	phone = db.Column(db.Unicode(32))
	city = db.Column(db.Unicode(128))
	country = db.Column(db.Unicode(128))
	notes = db.Column(db.UnicodeText)

	def add(self,first_name,email,username,password):
		try:
			self.first_name=first_name
			self.email=email
			self.username=username
			self.password=password
			#db.db.session.add(self)
			#db.db.session.commit()
			return self
		except:
			print('add_error')
			return

class Articles(db.Model):
	id =  db.Column(db.Integer, primary_key=True)
	#self.id, self.title,self.body,self.author = cursor
	title=  db.Column(db.Unicode(64))
	body =  db.Column(db.UnicodeText)
	author = db.Column(db.Unicode(64))
	date = db.Column(db.Unicode(64))
	def add(self,title,body,author):
		try:
			self.title=title
			self.body=body
			self.author=author
			#db.db.session.add(self)
			#db.db.session.commit()
			return self
		except:
			print('add_error')
			return

class Templates(db.Model):
	id =  db.Column(db.Integer, primary_key=True)
	#self.id, self.title,self.body,self.author = cursor
	name=  db.Column(db.Unicode(64))
	body =  db.Column(db.UnicodeText)
	param = db.Column(db.Unicode(128))
	link = db.Column(db.Unicode(128))
	def add(self,name,body='',param='',link=''):
		try:
			self.name=name
			self.body=body
			self.param=param
			self.link=link
			#db.db.session.add(self)
			#db.db.session.commit()
			return self
		except:
			print('add_error')
			return

class File(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Unicode(64))
	path = db.Column(db.Unicode(128))
	def add(self,name,path=''):
		try:
			self.name=name
			self.path=path
			#db.db.session.add(self)
			#db.db.session.commit()
			return self
		except:
			print('add_error')
			return
	def __unicode__(self):
		return self.name


class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Unicode(64))
	path = db.Column(db.Unicode(128))
	#path1= db.Column(db.Unicode(128))
	def add(self,name,path=''):
		try:
			self.name=name
			self.path=path
			#db.db.session.add(self)
			#db.db.session.commit()
			return self
		except:
			print('add_error')
			return
	def __unicode__(self):
		return self.name

'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(64))
    last_name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(128))
    phone = db.Column(db.Unicode(32))
    city = db.Column(db.Unicode(128))
    country = db.Column(db.Unicode(128))
    notes = db.Column(db.UnicodeText)
'''
class User1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(64))
    last_name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(128))
    phone = db.Column(db.Unicode(32))
    city = db.Column(db.Unicode(128))
    country = db.Column(db.Unicode(128))
    path = db.Column(db.Unicode(128))
    notes = db.Column(db.UnicodeText)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    body = db.Column(db.UnicodeText)

    def __unicode__(self):
        return self.name

########
def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import random
    import string

    db.drop_all()
    db.create_all()

    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]
    locations = [
        ("Shanghai", "China"),
        ("Istanbul", "Turkey"),
        ("Karachi", "Pakistan"),
        ("Mumbai", "India"),
        ("Moscow", "Russia"),
        ("Sao Paulo", "Brazil"),
        ("Beijing", "China"),
        ("Tianjin", "China"),
        ("Guangzhou", "China"),
        ("Delhi", "India"),
        ("Seoul", "South Korea"),
        ("Shenzhen", "China"),
        ("Jakarta", "Indonesia"),
        ("Tokyo", "Japan"),
        ("Mexico City", "Mexico"),
        ("Kinshasa", "Democratic Republic of the Congo"),
        ("Bangalore", "India"),
        ("New York City", "United States"),
        ("London", "United Kingdom"),
        ("Bangkok", "Thailand"),
        ("Tehran", "Iran"),
        ("Dongguan", "China"),
        ("Lagos", "Nigeria"),
        ("Lima", "Peru"),
        ("Ho Chi Minh City", "Vietnam"),
        ]

    for i in range(len(first_names)):
        user = Users()
        user.first_name = first_names[i]
        user.last_name = last_names[i]
        user.email = user.first_name.lower() + "@example.com"
        tmp = ''.join(random.choice(string.digits) for i in range(10))
        user.phone = "(" + tmp[0:3] + ") " + tmp[3:6] + " " + tmp[6::]
        user.city = locations[i][0]
        user.country = locations[i][1]
        db.session.add(user)

    for i in range(len(first_names)):
        user1 = User1()
        user1.first_name = first_names[i]
        user1.last_name = last_names[i]
        user1.email = user.first_name.lower() + "@example.com"
        tmp = ''.join(random.choice(string.digits) for i in range(10))
        user1.phone = "(" + tmp[0:3] + ") " + tmp[3:6] + " " + tmp[6::]
        user1.city = locations[i][0]
        user1.country = locations[i][1]
        db.session.add(user1)

    images = ["Buffalo", "Elephant", "Leopard", "Lion", "Rhino"]
    for name in images:
        image = Image()
        image.name = name
        image.path = name.lower() + ".jpg"
        db.session.add(image)

    for i in [1, 2, 3]:
        file = File()
        file.name = "Example " + str(i)
        file.path = "example_" + str(i) + ".pdf"
        db.session.add(file)

    sample_text = "<h1>About Us</h1>" + \
    "<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>"
    db.session.add(Page(name="About", body=sample_text))

    db.session.commit()
    return

#db.create_all()
# Build a sample db on the fly, if one does not exist yet.
database_path = os.path.join(ROOT_DIR, app.config['DATABASE_FILE'])
if not os.path.exists(database_path):
	build_sample_db()
	print(database_path)
#########################

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
'''
def log_the_user_in(username):
    return render_template('profile.html', username=username)

def register_user(name, email, username, password):
    query_db("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",(name, email, username, password))
    get_db().commit()

#import form menu.py >>
#cur.execute("CREATE TABLE IF NOT EXISTS users(name text, email string, username string, password string)")
#cur.execute("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",(name, email, username, password))

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
#from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import sqlite3
from flask import g

app = Flask(__name__)

# Config MySQL
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '123456'
#app.config['MYSQL_DB'] = 'myflaskapp'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#app.config['DATABASE']='Dev.db'
app.config['DATABASE']='Test.db'


#DATABASE = 'Dev.db'

# init MYSQL
#mysql = MySQL(app)

#Articles = Articles()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(app.config['DATABASE'])
		db.row_factory = sqlite3.Row
	return db
@app.teardown_appcontext
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
>>> from yourapplication import init_db
>>> init_db()
'''
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
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
    #user = query_db('select * from users where name = ? and password = ?', [username, password], one=True)
    user = query_db('select * from users where username = ?',[username], one=True)
    #if sha256_crypt.verify(password,user['password']):
    #    print("TRUE")
    #else:
    #    print("FALSE")
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
    #cur = get_db().cursor()
    #cur.execute("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",(name, email, username, password))
    get_db().commit()
    #cur.close()
			 
#import form menu.py >>
#cur.execute("CREATE TABLE IF NOT EXISTS users(name text, email string, username string, password string)")
#cur.execute("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",(name, email, username, password))
# Index

@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Articles
@app.route('/articles')
def articles():
    # Create cursor
    #cur = mysql.connection.cursor()
    #con = sqlite3.connect(DATABASE)
    #con.row_factory = dict_factory
    #cur=con.cursor()
	#with app.app_context():
	#cur = get_db().cursor()
	#Easy Querying
	for title in query_db('select * from articles_v'):
		print (title['title'], 'has the id', title['id'])
	#a single result:
	the_username='test1'
	user = query_db('select * from users where name = ?',[the_username], one=True)
	if user is None:
		print ('No such user')
	else:
			print (the_username, 'has the email', user['email'])
	####
	# Get articles
	try:
		articles =query_db("SELECT * FROM articles_v")
		#result = cur.execute("SELECT * FROM articles_v")
		#articles = cur.fetchall()
		#for article in articles:
			#print(article['title'])
			#print(article)
		#print(articles)
	except:
		#cur.close()
		#con.close()
		msg = 'No Articles Found'
		return render_template('articles.html', msg=msg)
	finally:
	# Close connection
		#cur.close()
		#con.close()
		if articles:
			return render_template('articles.html', articles=articles)
		else:
			msg = 'No Articles Found'
			return render_template('articles.html', msg=msg)
#Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    #cur = mysql.connection.cursor()
    #con = sqlite3.connect(DATABASE)
    #con.row_factory = dict_factory
    #cur=con.cursor()
	#with app.app_context():
	#cur = get_db().cursor()
	# Get article
	try:
		article =query_db("SELECT * FROM articles_v WHERE id = ?",[id],one=True)
		#result = cur.execute("SELECT * FROM articles_v WHERE id = ?", [id])
		#article = cur.fetchone()
	except:
		#cur.close()
		#con.close()
		msg = 'No Articles Found'
		return render_template('articles.html', msg=msg)
	finally:
		#cur.close()
		#con.close()
		return render_template('article.html', article=article)

## Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])
#Template Form class
class TemplateForm(Form):
    name = StringField('Name')
    body = TextAreaField('Body')
    param = TextAreaField('Parameters')
    link = StringField('Link')
# User Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        password = sha256_crypt.encrypt(str(form.password.data))
        print('test')
        register_user(request.form['name'], request.form['email'], request.form['username'],password)
        #get_db().commit()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))


    return render_template('register.html', form=form)
#LOGIN
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            #return log_the_user_in(request.form['username'])
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username/password'


    return render_template('login.html', error=error)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            session['database'] = app.config['DATABASE']
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	#with app.app_context():
	#cur = get_db().cursor()
	# Create cursor
	#cur = mysql.connection.cursor()
	#con = sqlite3.connect(DATABASE)
	#con.row_factory = dict_factory
	#cur=con.cursor()
	# Get articles
	try:
		#result = cur.execute("SELECT * FROM articles_v")
		#articles = cur.fetchall()
		articles =query_db("SELECT * FROM articles_v")
	except:
		#cur.close()
		#con.close()
		msg = 'No Articles Found'
		return render_template('dashboard.html', msg=msg)
	finally:
	# Close connection
		#cur.close()
		#con.close()
		if articles:
			return render_template('dashboard.html', articles=articles)
		else:
			msg = 'No Articles Found'
			return render_template('dashboard.html', msg=msg)

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	#with app.app_context():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data
	
		# Create Cursor
		#cur = mysql.connection.cursor()
		#con = sqlite3.connect(DATABASE)
		#con.row_factory = dict_factory
		#cur=con.cursor()
		#cur = get_db().cursor()
		# Execute
		try:
			#cur.execute("CREATE TABLE IF NOT EXISTS articles_v(id INTEGER PRIMARY KEY,title text, body string, author string)")
			#cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))
			#cur.execute("INSERT INTO articles_v(title, body, author) VALUES(?, ?, ?)",(title, body, session['username']))
			query_db("INSERT INTO articles_v(title, body, author) VALUES(?, ?, ?)",(title, body, session['username']))
	
			# Commit to DB
			#mysql.connection.commit()
			get_db().commit()
			#Close connection
			#cur.close()
			#con.close()
			flash('Article Created', 'success')
		except:
			#cur.close()
			app.logger.info('CREATE ERROR')
			#cur.close()
			error = 'CREATE ERROR'
			return render_template('home.html', error=error)	
	
		return redirect(url_for('dashboard'))
	
	return render_template('add_article.html', form=form)

# Edit Template
@app.route('/edit_/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_(id):
	#with app.app_context():
	print('START...')
	# Create cursor
	#cur = mysql.connection.cursor()
	#con = sqlite3.connect(DATABASE)
	#con.row_factory = dict_factory
	#cur=con.cursor()
	#cur = get_db().cursor()
	# Get article by id
	try:
		print('START TRY...')
		#result = cur.execute("SELECT * FROM template WHERE id = ?", [id])
		#article = cur.fetchone()
		article=query_db("SELECT * FROM template WHERE id = ?", [id],one=True)
		#cur.close()
		print(article['name'])
		#con.close()
		# Get form
		form = TemplateForm(request.form)
	
		# Populate article form fields
		form.name.data=article['name']
		form.body.data = article['body']
		form.param.data = article['param']
		form.link.data = article['link']
	except:
		print('Error')
		#cur.close()
		error = 'No Template Found'
		return render_template('home.html', error=error)
	if request.method == 'POST' and form.validate():
		name = request.form['name']
		body = request.form['body']
		param = request.form['param']
		link = request.form['link']
	
		# Create Cursor
		#cur = mysql.connection.cursor()
		#con = sqlite3.connect(DATABASE)
		#con.row_factory = dict_factory
		#cur=con.cursor()
		#cur = get_db().cursor()
		app.logger.info(name)
		try:
			# Execute
			#cur.execute ("UPDATE template SET name=?, body=?, param=?, link=? WHERE id=?",(name, body,param,link, id))
			query_db("UPDATE template SET name=?, body=?, param=?, link=? WHERE id=?",(name, body,param,link, id))
			# Commit to DB
			#mysql.connection.commit()
			get_db().commit()
			#Close connection
			#cur.close()
		except:
			app.logger.info('UPDATE ERROR')
			#cur.close()
			error = 'UPDATE ERROR'
			return render_template('home.html', error=error)				
		#con.close()
		#cur.close()
		flash('Template Updated', 'success')
		return redirect(url_for('index'))
	#cur.close()
	return render_template('edit_.html', form=form)

# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
	#with app.app_context():
	# Create cursor
	#cur = mysql.connection.cursor()
	#con = sqlite3.connect(DATABASE)
	#con.row_factory = dict_factory
	#cur=con.cursor()
	#cur = get_db().cursor()
	# Get article by id
	try:
		#result = cur.execute("SELECT * FROM articles_v WHERE id = ?", [id])
		#article = cur.fetchone()
		article =query_db("SELECT * FROM articles_v WHERE id = ?", [id],one=True)
		#cur.close()
		#con.close()
		# Get form
		form = ArticleForm(request.form)
		
		# Populate article form fields
		form.title.data = article['title']
		form.body.data = article['body']
	except:
		print('Error')
		#cur.close()
		error = 'No Article Found'
		return render_template('home.html', error=error)		
	
	
	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']
	
		# Create Cursor
		#cur = mysql.connection.cursor()
		#con = sqlite3.connect(DATABASE)
		#con.row_factory = dict_factory
		#cur=con.cursor()
		#cur = get_db().cursor()
	
		app.logger.info(title)
		try:
			# Execute
			#cur.execute ("UPDATE articles_v SET title=?, body=? WHERE id=?",(title, body, id))
			query_db("UPDATE articles_v SET title=?, body=? WHERE id=?",(title, body, id))
			# Commit to DB
			#mysql.connection.commit()
			get_db().commit()
			#Close connection
			#cur.close()
		except:
			app.logger.info('UPDATE ERROR')
			#cur.close()
			error = 'UPDATE ERROR'
			return render_template('home.html', error=error)				
		#con.close()
	
		flash('Article Updated', 'success')
		#cur.close()
		return redirect(url_for('dashboard'))
	#cur.close()
	return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
	#with app.app_context():
	# Create cursor
	#cur = mysql.connection.cursor()
	#con = sqlite3.connect(DATABASE)
	#con.row_factory = dict_factory
	#cur=con.cursor()
	#cur = get_db().cursor()
	try:
		# Execute
		#cur.execute("DELETE FROM articles_v WHERE id = ?", [id])
		query_db("DELETE FROM articles_v WHERE id = ?", [id])
		# Commit to DB
		#mysql.connection.commit()
		get_db().commit()
		#Close connection
		#cur.close()
		#con.close()
		flash('Article Deleted', 'success')
	except:
		app.logger.info('Delete ERROR')
		#cur.close()
		error = 'DELETE ERROR'
		return render_template('home.html', error=error)			
	
	return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)

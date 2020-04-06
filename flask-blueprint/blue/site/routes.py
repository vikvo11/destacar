


'''
@mod.route('/homepage')
def homepage():
	return render_template('site/index.html')
'''
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask import jsonify
#from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


#from __name__ import query_db
from blue import app
#from blue.site.database import get_db,query_db,init_db,valid_login,log_the_user_in,register_user
from blue.site import database as db
from blue.site import classes as cls
#import config
from flask import Blueprint
mod = Blueprint('site', __name__, template_folder='templates')
#mod = Flask(__name__)

# Config DB
#mod.config['DATABASE']='Dev.db'
#app.config['DATABASE']='blue/site/Test.db'



# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            session['database'] = app.config['DATABASE']
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('site.login'))
    return wrap

# Index

@mod.route('/')
def index():
    return render_template('home.html')


# About
@mod.route('/about')
def about():
    return render_template('about.html')


# Articles
@mod.route('/articles')
def articles():
	#Easy Querying
	for title in db.query_db('select * from articles_v'):
		print (title['title'], 'has the id', title['id'])
	#a single result:
	the_username='test1'
	user = db.query_db('select * from users where name = ?',[the_username], one=True)
	if user is None:
		print ('No such user')
	else:
			print (the_username, 'has the email', user['email'])
	####
	# Get articles
	try:
		#articles =db.query_db("SELECT * FROM articles_v")
		articles=cls.Articles.fetchall().list
	except:
		msg = 'No Articles Found'
		return render_template('articles.html', msg=msg)

	if articles:
		return render_template('articles.html', articles=articles)
	else:
		msg = 'No Articles Found'
		return render_template('articles.html', msg=msg)
#Single Article
@mod.route('/article/<string:id>/')
def article(id):
	try:
		#article =db.query_db("SELECT * FROM articles_v WHERE id = ?",[id],one=True)
		article=cls.Articles.fetchone(id=id,where='id')
	except:
		msg = 'No Articles Found'
		return render_template('articles.html', msg=msg)
	finally:
		return render_template('article.html', article=article)
# User Register
@mod.route('/register', methods=['POST', 'GET'])
def register():
    form = cls.RegisterForm(request.form)
    if request.method == 'POST':#and form.validate():
        password = sha256_crypt.encrypt(str(form.password.data))
        print('test')
        db.register_user(request.form['name'], request.form['email'], request.form['username'],password)
        #db.get_db().commit()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('site.login'))


    return render_template('register.html', form=form)
#LOGIN
@mod.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if db.valid_login(request.form['username'], request.form['password']):
            #return db.log_the_user_in(request.form['username'])
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You are now logged in', 'success')
            return redirect(url_for('site.dashboard'))
        else:
            error = 'Invalid username/password'


    return render_template('login.html', error=error)



# Logout
@mod.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('site.login'))

# Dashboard
@mod.route('/dashboard')
@is_logged_in
def dashboard():
	try:
		#articles =db.query_db("SELECT * FROM articles_v")
		articles=cls.Articles.fetchall().list
		#test=cls.Articles.fetchone(id='3',where='id')
	except:
		msg = 'No Articles Found'
		return render_template('dashboard.html', msg=msg)

	if articles:
		return render_template('dashboard.html', articles=articles)
	else:
		msg = 'No Articles Found'
		return render_template('dashboard.html', msg=msg)

# Add Article
@mod.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	#with mod.app_context():
	form = cls.ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		body = form.body.data
		try:
			#db.query_db("INSERT INTO articles_v(title, body, author) VALUES(?, ?, ?)",(title, body, session['username']))
			#article=cls.Articles()
			#article.add('title, body, author',"'{}','{}','{}'".format(title,body,session['username']))
			article=cls.Articles().add('title, body, author',"'{}','{}','{}'".format(title,body,session['username']))
			#db.get_db().commit()
			flash('Article Created', 'success')
		except:
			app.logger.info('CREATE ERROR')
			error = 'CREATE ERROR'
			return render_template('home.html', error=error)

		return redirect(url_for('site.dashboard'))

	return render_template('add_article.html', form=form)

# Edit Article
@mod.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
	#with mod.app_context():
	try:
		#article =db.query_db("SELECT * FROM articles_v WHERE id = ?", [id],one=True)
		article=cls.Articles.fetchone(id=id,where='id')
		form = cls.ArticleForm(request.form)

		# Populate article form fields
		form.title.data = article.title
		form.body.data = article.body
	except:
		print('Error')
		error = 'No Article Found'
		return render_template('home.html', error=error)


	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']

		app.logger.info(title)
		try:
			# Execute
			#db.query_db("UPDATE articles_v SET title=?, body=? WHERE id=?",(title, body, id))
			#db.get_db().commit()
			article.update(set="title='{}',body='{}'".format(title,body),id=article.id,where='id')
		except:
			app.logger.info('UPDATE ERROR')
			error = 'UPDATE ERROR'
			return render_template('home.html', error=error)

		flash('Article Updated', 'success')
		return redirect(url_for('site.dashboard'))
	return render_template('edit_article.html', form=form)

# Delete Article
@mod.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
	#with mod.app_context():
	try:
		# Execute
		#db.query_db("DELETE FROM articles_v WHERE id = ?", [id])
		#article=cls.Articles()

		#article=cls.Articles.fetchone(id=id,where='id')
		#article.delete(article.id)
		article=cls.Articles().delete(id)
		#db.get_db().commit()
		flash('Article Deleted', 'success')
	except:
		app.logger.info('Delete ERROR')
		error = 'DELETE ERROR'
		return render_template('home.html', error=error)

	return redirect(url_for('site.dashboard'))

# Edit Template
@mod.route('/edit_template/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_(id):
	#with mod.app_context():
	try:
		#article=db.query_db("SELECT * FROM template WHERE id = ?", [id],one=True)
		template=cls.Templates.fetchone(id=id,where='id')
		form = cls.TemplateForm(request.form)

		# Populate article form fields
		form.name.data=template.name
		form.body.data = template.body
		form.param.data = template.param
		form.link.data = template.link
	except:
		print('Error')
		error = 'No Template Found'
		return render_template('home.html', error=error)
	if request.method == 'POST' and form.validate():
		name = request.form['name']
		body = request.form['body']
		param = request.form['param']
		link = request.form['link']
		app.logger.info(name)
		try:
			template.update(set="name='{}',body='{}',param='{}',link='{}'".format(name,body,param,template.name),id=template.id,where='id')
			#db.query_db("UPDATE template SET name=?, body=?, param=?, link=? WHERE id=?",(name, body,param,link, id))
			#db.get_db().commit()
		except:
			app.logger.info('UPDATE ERROR')
			error = 'UPDATE ERROR'
			return render_template('home.html', error=error)
		flash('Template Updated', 'success')
		return redirect(url_for('site.index'))
	return render_template('edit_.html', form=form)

#for Testing
@mod.route("/dummy")
def dummy():
    return jsonify({"dummy":"dummy-value"})

@mod.route('/error', methods=['GET','POST'])
def error():
	app.logger.info('Delete ERROR')
	error = 'DELETE ER1ROR'
	return render_template('home.html', error=error)

@mod.route('/homepage')
def homepage():


	#test1=cls.Articles.fetchall()
	#test=cls.Articles.fetchone(id='3',where='id')

	#print(test1.__dict__)
	#print(test.__dict__)

	#test.set_table_select('articles_v','title,id,body,author')
	#test.table,test.select='articles_v','title,id,body,author';
	#print('table={}, select={}'.format(test.table,test.select))
	#test2=cls.Articles.fetchone(id='3',where='id')
	#print(test.fetchone(id='4',where='id').__dict__)
	#print('table={}, select={}'.format(test.table,test.select))
	#print('table={}, select={}'.format(test2.table,test2.select))
	#print(test.__dict__)
	#print(test2.__dict__)
	#test=db.query_db("SELECT id,title,author,body FROM articles_v WHERE id = ?",[3],one=True)
	#test=cls.Article(db.query_db("SELECT id,title,author,body FROM {} WHERE id = {}".format('articles_v',4),one=True))

	#if test is not None: print(test.__dict__)


	#cur.execute("SELECT name, bday FROM employees WHERE empid = ?", (empid,))
	#self,name, self.bday = cur.fetchone()
	#print(db.query_db("SELECT id,title,author,body FROM articles_v WHERE id = ?",[3],one=True)['body'])
	#return render_template('article.html', article=test)
	return render_template('site/index.html')
#if __name__ == '__main__':
#    app.secret_key='secret123'
#    app.run(debug=True)

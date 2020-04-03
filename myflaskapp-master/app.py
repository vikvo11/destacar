from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
#from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import sqlite3

app = Flask(__name__)

# Config MySQL
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '123456'
#app.config['MYSQL_DB'] = 'myflaskapp'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
DATABASE = 'Dev.db'

# init MYSQL
#mysql = MySQL(app)

#Articles = Articles()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#import form menu.py >>
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
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur=con.cursor()

    # Get articles
    try:
        result = cur.execute("SELECT * FROM articles_v")
        articles = cur.fetchall()
        for article in articles:
            #print(article['title'])
            print(article)
        #print(articles)
    except:
        cur.close()
        con.close()
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    finally:
    # Close connection
        cur.close()
        con.close()
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
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur=con.cursor()
    # Get article
    try:
        result = cur.execute("SELECT * FROM articles_v WHERE id = ?", [id])
        article = cur.fetchone()
    except:
        cur.close()
        con.close()
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    finally:
        cur.close()
        con.close()
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
    name = StringField('Name', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body')
    param = TextAreaField('Parameters', [validators.Length(min=0)])
    link = StringField('Link', [validators.Length(min=0, max=200)])


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        #cur = mysql.connection.cursor()
        con = sqlite3.connect(DATABASE)
        con.row_factory = dict_factory
        cur=con.cursor()

        # Execute query
        cur.execute("CREATE TABLE IF NOT EXISTS users(name text, email string, username string, password string)")
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",(name, email, username, password))

        # Commit to DB
        #mysql.connection.commit()
        con.commit()

        # Close connection
        #cur.close()
        con.close()
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form.get('username'))
        print(request.form.get('password'))
        # Get Form Fields
        #username = request.form['username']
        #password_candidate = request.form['password']
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Create cursor
        #cur = mysql.connection.cursor()
        con = sqlite3.connect(DATABASE)
        con.row_factory = dict_factory
        cur=con.cursor()
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = ?", [username])
        data = cur.fetchone()
        print(data)
        #if result > 0:
        if data:
            # Get stored hash
            #data = cur.fetchone()
            #password = data['password']
            password = data['password']
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
            con.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
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
    # Create cursor
    #cur = mysql.connection.cursor()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur=con.cursor()
    # Get articles
    try:
        result = cur.execute("SELECT * FROM articles_v")
        articles = cur.fetchall()
    except:
        cur.close()
        con.close()
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    finally:
    # Close connection
        cur.close()
        con.close()
        if articles:
            return render_template('dashboard.html', articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('dashboard.html', msg=msg)

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        #cur = mysql.connection.cursor()
        con = sqlite3.connect(DATABASE)
        con.row_factory = dict_factory
        cur=con.cursor()
        # Execute
        cur.execute("CREATE TABLE IF NOT EXISTS articles_v(id INTEGER PRIMARY KEY,title text, body string, author string)")
        #cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))
        cur.execute("INSERT INTO articles_v(title, body, author) VALUES(?, ?, ?)",(title, body, session['username']))

        # Commit to DB
        #mysql.connection.commit()
        con.commit()
        #Close connection
        cur.close()
        con.close()
        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)

# Edit Article
@app.route('/edit_/<string:id>', methods=['GET', 'POST'])
#@is_logged_in
def edit_(id):
    # Create cursor
    #cur = mysql.connection.cursor()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur=con.cursor()
    # Get article by id
    try:
        result = cur.execute("SELECT * FROM template WHERE id = ?", [id])
        article = cur.fetchone()
        print(article['name'])
    except:
        print('Error')
    finally:

        cur.close()
        con.close()
    # Get form
    form = TemplateForm(request.form)

    # Populate article form fields
    form.name.data=article['name']
    form.body.data = article['body']
    form.param.data = article['param']
    form.link.data = article['link']

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        body = request.form['body']
        param = request.form['param']
        link = request.form['link']

        # Create Cursor
        #cur = mysql.connection.cursor()
        con = sqlite3.connect(DATABASE)
        con.row_factory = dict_factory
        cur=con.cursor()

        app.logger.info(name)
        # Execute
        cur.execute ("UPDATE template SET name=?, body=?, param=?, link=? WHERE id=?",(name, body,param,link, id))
        # Commit to DB
        #mysql.connection.commit()
        con.commit()
        #Close connection
        cur.close()
        con.close()

        flash('Template Updated', 'success')

        return redirect(url_for('index'))

    return render_template('edit_.html', form=form)

# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    #cur = mysql.connection.cursor()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur=con.cursor()
    # Get article by id
    result = cur.execute("SELECT * FROM articles_v WHERE id = ?", [id])

    article = cur.fetchone()
    cur.close()
    con.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        #cur = mysql.connection.cursor()
        con = sqlite3.connect(DATABASE)
        con.row_factory = dict_factory
        cur=con.cursor()

        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE articles_v SET title=?, body=? WHERE id=?",(title, body, id))
        # Commit to DB
        #mysql.connection.commit()
        con.commit()
        #Close connection
        cur.close()
        con.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    #cur = mysql.connection.cursor()
    con = sqlite3.connect(DATABASE)
    con.row_factory = dict_factory
    cur=con.cursor()
    # Execute
    cur.execute("DELETE FROM articles_v WHERE id = ?", [id])

    # Commit to DB
    #mysql.connection.commit()
    con.commit()
    #Close connection
    cur.close()
    con.close()
    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)

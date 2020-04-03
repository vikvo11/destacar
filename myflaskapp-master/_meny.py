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
    con = sqlite3.connect("Test.db")
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
    con = sqlite3.connect("Test.db")
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

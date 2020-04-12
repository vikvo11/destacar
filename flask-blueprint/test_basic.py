import os
import re
import unittest
import sqlite3
#from app import app,query_db
from blue import app
#from blue.site.routes import query_db
from blue.site import database as db
from flask import g
import random
import string
import json


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def assertTrue(self,response):
    self.assertNotEqual(response.status_code, 404)
    self.assertFalse(re.search('ERROR',response.get_data(as_text=True)))
    self.assertFalse(re.search('Invalid',response.get_data(as_text=True)))
    return

TEST_DB = 'myblog_test.sqlite'
app.config['DATABASE']='blue/site/Test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        #import config
        #from database import db
        app.config['TESTING'] = True
        #app.config['WTF_CSRF_ENABLED'] = False
        #app.config['DEBUG'] = False
        app.secret_key='secret123'
        self.app = app.test_client()
        #db.drop_all()
        #db.create_all()

        # Disable sending emails during unit testing
        #mail.init_app(app)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


###############
#### tests ####
###############

    def test_main_page(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['logged_in'] = True
                session['username'] = 'Test'
        response = self.app.get('/edit_template/1', follow_redirects=True)
        assertTrue(self,response)
        print(response.data)

    def test_register_login(self):
        #with app.app_context():
            #for user in db.query_db('select * from users'):
               # print(user['name'])
        with app.test_client() as c:
            #app.config['DATABASE']='Test.db'
            #app.config['DATABASE']='blue/site/Test.db'
            for x in range(1):
                name=randomString(10)
                passw=randomString(10)
                sent = {'name':'test'+str(x),'email':'email@email'+str(x),'username':name,'password':passw}
                print(sent)
                response = c.post('/register',data=sent)
                sent = {'username':name,'password':passw}
                request = c.post('/login',data=sent)
                print(request.data)
            # check result from server with expected data
                assertTrue(self,response)
                assertTrue(self,request)

    def test_main(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {'username':'test','password':'test'}
            response = client.post(
                '/login',
                data=sent
            )
            print(response.data)
            assertTrue(self,response)

    def test_add_article(self):
        #app.config['DATABASE']='blue/site/Test.db'
        with app.app_context():
            for user in db.query_db('select * from users'):
                print(user['name'])
        with app.test_client() as c:
            #app.config['DATABASE']='blue/site/Test.db'
            with c.session_transaction() as session:
                session['logged_in'] = True
                session['username'] = 'Test'
            # send data as POST form to endpoint

            for x in range(5):
                sent = {'title':'test'+str(x),'body':'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'}
                response = c.post('/add_article',data=sent)
            # check result from server with expected data
                print(response.data)
                assertTrue(self,response)

    def test_edit_article(self):
        #app.config['DATABASE']='blue/site/Test.db'
        with app.app_context():
            articles=db.query_db('select * from articles_v')
        with app.test_client() as c:

            with c.session_transaction() as session:
                session['logged_in'] = True
                session['username'] = 'Test'
            # send data as POST form to endpoint
            for article in articles:
                print(article['id'],article['body'])
                sent = {'title':'EDIT'+str(article['id']),'body':str(article['body'])+'-EDIT'}
                response = c.post('/edit_article/'+str(article['id']),data=sent)
            # check result from server with expected data
                assertTrue(self,response)

    def test_open_article(self):
        with app.app_context():
            #articles=db.query_db('select * from articles_v')
            articles = db.Articles().query.all()
            #for article in articles:
                #print(article['id'])
        with app.test_client() as c:
            #c.DATABASE = 'Test.db'
            #app.config['DATABASE']='blue/site/Test.db'
            #c.config['DATABASE']='Test.db'
            with c.session_transaction() as session:
                session['logged_in'] = True
                session['username'] = 'Test'
            # send data as POST form to endpoint
            for article in articles:
                print(article.id)
                print('/article/'+str(article['id']))
                response = self.app.get('/article/'+str(article.id), follow_redirects=True)
                print(response.data)
                assertTrue(self,response)

    def test_delete_article(self):
        with app.app_context():
            #articles=db.query_db('select * from articles_v')
            articles = db.Articles().query.all()
            #for article in articles:
                #print(article['id'])
        with app.test_client() as c:
            #app.config['DATABASE']='blue/site/Test.db'
            with c.session_transaction() as session:
                session['logged_in'] = True
                session['username'] = 'Test'
            # send data as POST form to endpoint
            for article in articles:
                #print(article['id'])
                #sent = {'title':'EDIT'+str(article['id']),'body':str(article['body'])+'-EDIT'}
                response = c.post('/delete_article/'+str(article.id))
                print(response.data)
                assertTrue(self,response)

	#JSON test
    def test_dummy(self):
        response = self.app.get("/dummy")
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['dummy'], "dummy-value")
        assertTrue(self,response)

	#Find ERROR msg
    def test_error(self):
        response = self.app.get("/error")
        print(response.data)
        app.config['DATABASE']='blue/site/Test.db'
        print(app.config['DATABASE'])
        assertTrue(self,response)
'''
def CheckSqliteRowHashCmp(self):
        """Checks if the row object compares and hashes correctly"""
        self.con.row_factory = sqlite.Row
        row_1 = self.con.execute("select 1 as a, 2 as b").fetchone()
        row_2 = self.con.execute("select 1 as a, 2 as b").fetchone()
        row_3 = self.con.execute("select 1 as a, 3 as b").fetchone()

        self.assertEqual(row_1, row_1)
        self.assertEqual(row_1, row_2)
        self.assertTrue(row_2 != row_3)

        self.assertFalse(row_1 != row_1)
        self.assertFalse(row_1 != row_2)
        self.assertFalse(row_2 == row_3)

        self.assertEqual(row_1, row_2)
        self.assertEqual(hash(row_1), hash(row_2))
        self.assertNotEqual(row_1, row_3)
        self.assertNotEqual(hash(row_1), hash(row_3))
'''				
if __name__ == "__main__":
    unittest.main()

### python -m unittest -q test_basic.BasicTests.test_add_article

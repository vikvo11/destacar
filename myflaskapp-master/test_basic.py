import os
import unittest
#from flask import Flask

from app import app
#app = Flask(__name__)

#from blog.views import app as app1
#app.register_blueprint(app1)

TEST_DB = 'myblog_test.sqlite'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        #import config
        #from database import db
        #app.config['TESTING'] = True
        #app.config['WTF_CSRF_ENABLED'] = False
        #app.config['DEBUG'] = False
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myblog_test.sqlite'
        #DATABASE = 'Dev1.db'
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
    '''
    def test_main_page(self):
        response = self.app.get('/edit_/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.data)

    '''
    def test_main(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {'username':'test','password':'test'}
            result = client.post(
                '/login',
                data=sent
            )
            # check result from server with expected data
            #self.assertEqual(
            #    result.data,
            #    json.dumps(sent)
            #)
            print(result.data)
            #self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()

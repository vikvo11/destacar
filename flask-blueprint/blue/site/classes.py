from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from blue import database as db
###SQLAlchemy



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
    body = TextAreaField('Body', [validators.Length(min=0)])
#Template Form class
class TemplateForm(Form):
    name = StringField('Name')
    body = TextAreaField('Body')
    param = TextAreaField('Parameters')
    link = StringField('Link')
'''
class Uploaded_files():
   @staticmethod
    def upd(name,path):
        try:
            file = db.File()
            #self.id, self.title,self.body,self.author = cursor
            file.name=name
            file.path=path
            db.db.session.add(file)
            db.db.session.commit()
            return file #'Done'#cls(cursor,list=True)
        except:
            print('test_error')
            return 'Error'
'''

class init_table():
    """docstring for init_table."""
    def __init__(self, arg=None,list=False):
        if list:
            self.list= arg
            print('List=True')
        else:
            print('List=False')
            if arg is not None: self.arg = arg
    @classmethod
    def fetchone(cls,id,where='id'):
        try:
            print(cls.table)
            print(cls.select)
            cursor=db.query_db("SELECT {} FROM {} WHERE {} = '{}'".format(cls.select,cls.table,where,id),one=True)
            print("SELECT {} FROM {} WHERE {} = '{}'".format(cls.select,cls.table,where,id))
            return cls(cursor)
        except:
            print('error')
            return
    @classmethod
    def fetchall(cls,id=1,where=1):
        try:
            print(cls.table)
            print(cls.select)
            print("SELECT {} FROM {} WHERE {} = {}".format(cls.select,cls.table,where,id))
            cursor=db.query_db("SELECT {} FROM {} WHERE {} = {}".format(cls.select,cls.table,where,id))
            print('teset')
            return cls(cursor,list=True)
        except:
            print('error')
            return
    @classmethod
    def set_table_select(cls,table,select='*'):
        cls.table=table
        cls.select=select
    #UPDATE
    #@staticmethod

    def add(self,into,value):
        try:
            print("INSERT INTO {}({}) VALUES({})".format(self.table, into,value))
            #db.query_db("UPDATE {} SET {} WHERE {} = '{}'".format(self.table, set,where,id)) #name=?, body=?, param=?, link=?
            db.query_db("INSERT INTO {}({}) VALUES({})".format(self.table, into,value))
            print('add')
            db.get_db().commit()
            print('add')
            return #cls(cursor,list=True)
        except:
            print('add_error')
            return

    def update(self,set,id,where='id'):
        try:
            print('{},{},{},{}'.format(self.table, set,where,id))
            print("UPDATE {} SET {} WHERE {} = '{}'".format(self.table, set,where,id))
            db.query_db("UPDATE {} SET {} WHERE {} = '{}'".format(self.table, set,where,id)) #name=?, body=?, param=?, link=?
            print('update')
            db.get_db().commit()
            print('update')
            return #cls(cursor,list=True)
        except:
            print('update_error')
            return

    def delete(self,id,where='id'):
        try:
            #print('{},{},{},{}'.format(self.table, set,where,id))
            print("DELETE FROM {} WHERE {} = '{}'".format(self.table,where,id))
            #db.query_db("UPDATE {} SET {} WHERE {} = '{}'".format(self.table, set,where,id)) #name=?, body=?, param=?, link=?
            db.query_db("DELETE FROM {} WHERE {} = '{}'".format(self.table,where,id))
            print('delete')
            db.get_db().commit()
            print('delete')
            return #cls(cursor,list=True)
        except:
            print('delete_error')
            return

    def test(self,view):
        try:
            #for i in [1, 2, 3]:
            #    view = File()
            #    view.name = "Example1 " + str(i)
            #    print(view.name)
            #    view.path = "example_" + str(i) + ".pdf"
            #    db.db.session.add(view)
            #view.id=1
            #view.name='test'
            #view.path='path_test'

            #admin = User.query.filter_by(username='admin').first()
            #admin.email = 'my_new_email@example.com'
            #rows_changed = User.query.filter_by(role='admin').update(dict(permission='add_user'))
            #Notice that filter_by takes keyword arguments (use only one =) as opposed to filter which takes an expression.

            #user = view.query.get(1)
            #user.name = 'New Name123'
            #user = view.query.filter_by(id=3).first()
            #db.db.session.delete(user)
            #db.db.session.commit()

            user = db.Articles_new()
            #self.id, self.title,self.body,self.author = cursor
            user.title='test'
            user.body ='test'
            user.author ='test'
            db.db.session.add(user)
            db.db.session.commit()
            return 'Done'#cls(cursor,list=True)
        except:
            print('test_error')
            return 'Error'

class Articles_old(init_table):
    table='articles_v'
    select='id,title,body,author'
    def __init__(self,cursor=None,list=False):
        #super().__init__(cursor,list=False)
        if list:
            self.list= cursor
            print('List=True')
        else:
            print('List=False')
            if cursor is not None: self.id, self.title,self.body,self.author = cursor

class Templates(init_table):
    table='template'
    select='id,name,body,param,link'
    def __init__(self,cursor=None,list=False):
        #super().__init__(cursor,list=False)
        if list:
            self.list= cursor
            print('List=True')
        else:
            print('List=False')
            if cursor is not None: self.id, self.name,self.body,self.param,self.link = cursor

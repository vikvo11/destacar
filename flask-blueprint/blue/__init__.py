from flask import Flask
import os
import os.path as op
app = Flask(__name__)



from blue.api.routes import mod
from blue.site.routes import mod
from blue.admin.routes import mod
from blue.site.test import test
#from blue.site import config
#app.config['DATABASE']='Test.db'
app.config['DATABASE']='blue/site/Test.db'
#app.config['DATABASE']='blue/site/Dev.db'
app.secret_key='secret123'

#app_dir = op.realpath(os.path.dirname(__file__))
#file_path = op.join(app_dir, 'static','files')
#app.config['PATH_FILES']=file_path
#print('YRAAAAAAAAAAAAAAAAAAAAAA')
#print(app.config['PATH_FILES'])

app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod, url_prefix='/api')
app.register_blueprint(admin.routes.mod, url_prefix='/admin')


#root=sys.modules['__main__'].__file__

##Для быстрого открытия ресурсов из этого каталога можно воспользоваться функцией open_resource():
'''
with simple_page.open_resource('static/style.css') as f:
    code = f.read()
'''

with admin.routes.mod.open_resource('static/css/shop-homepage.css') as f:
    code = f.read()
print (code)

#test()

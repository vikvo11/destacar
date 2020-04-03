from flask import Flask

app = Flask(__name__)

from blue.api.routes import mod
from blue.site.routes import mod
from blue.admin.routes import mod
from blue.site.test import test
app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod, url_prefix='/api')
app.register_blueprint(admin.routes.mod, url_prefix='/admin')

##Для быстрого открытия ресурсов из этого каталога можно воспользоваться функцией open_resource():
'''
with simple_page.open_resource('static/style.css') as f:
    code = f.read()
'''

with admin.routes.mod.open_resource('static/css/shop-homepage.css') as f:
    code = f.read()
print (code)

test()

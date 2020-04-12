from flask import Flask
from flask import request,url_for
import os
import os.path as op
from blue.config import ROOT_DIR,file_path
app = Flask(__name__)

from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success

from blue.api.routes import mod
from blue.site.routes import mod
from blue.admin.routes import mod
from blue.site.test import test

#from blue.site import config
#app.config['DATABASE']='Test.db'
app.config['DATABASE']='blue/site/Test.db'
#app.config['DATABASE']='blue/site/Dev.db'
app.secret_key='secret123'


ckeditor = CKEditor(app)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 300
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['UPLOADED_PATH'] = file_path#os.path.join(ROOT_DIR, 'static','uploads')
#app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
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

@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    #print(path)
    return send_from_directory(path, filename)

''''''
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    url = url_for('static', filename='files/'+f.filename)
    #return
    return upload_success(url=url)

#test()

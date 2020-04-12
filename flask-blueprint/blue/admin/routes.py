from flask import Blueprint, render_template

import os
import os.path as op
import sys

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from wtforms import fields, widgets

from sqlalchemy.event import listens_for
from jinja2 import Markup

from flask_admin import Admin, form
from flask_admin.form import rules
from flask_admin.contrib import sqla, rediscli

from blue import app
#from blue.site import database
from blue.site.database import db
from blue import database
from blue.config import ROOT_DIR,file_path
from passlib.hash import sha256_crypt

#from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
#app = Flask(__name__, static_folder='files')
mod = Blueprint('admin1', __name__, template_folder='templates',static_folder='files')

# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


try:
    os.mkdir(file_path)
except OSError:
    pass


# Create models


# Delete hooks for models, delete files if models are getting deleted
@listens_for(database.File, 'after_delete')
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


@listens_for(database.Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

@listens_for(database.Users.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return sha256_crypt.encrypt(str(value))
    return value

# define a custom wtforms widget and field.
# see https://wtforms.readthedocs.io/en/latest/widgets.html#custom-widgets
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


# Administrative views
class PageView(sqla.ModelView):
    form_overrides = {
        'body': CKTextAreaField
    }
    create_template = 'create_page.html'
    edit_template = 'edit_page.html'

class ArticlesView(sqla.ModelView):
    form_overrides = {
        'body': CKTextAreaField
    }
    create_template = 'create_page.html'
    edit_template = 'edit_page.html'

class FileView(sqla.ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'path': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'path': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': False
        }
    }


class ImageView(sqla.ModelView):

    def _list_thumbnail(view, context, model, name):

        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename='files/'+form.thumbgen_filename(model.path)))
    def thumb_name(filename):
        name, _ = op.splitext(filename)
        return '%s-thumb123.jpg' % name


    column_formatters = {
        'path':_list_thumbnail,
		#'path':thumb_name

    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True),
									  endpoint='static',
									  url_relative_path='files/')
									  #,thumbgen=thumb_name)
    }


class UserView(sqla.ModelView):
    """
    This class demonstrates the use of 'rules' for controlling the rendering of forms.
    """
    form_create_rules = [
        # Header and four fields. Email field will go above phone field.
        rules.FieldSet(('first_name', 'last_name','username','password','email', 'phone'), 'Personal'),
        # Separate header and few fields
        rules.Header('Location'),
        rules.Field('city'),
        # String is resolved to form field, so there's no need to explicitly use `rules.Field`
        'country',
        # Show macro that's included in the templates
        rules.Container('rule_demo.wrap', rules.Field('notes'))
    ]

    # Use same rule set for edit page
    form_edit_rules = form_create_rules

    create_template = 'create_user.html'
    edit_template = 'edit_user.html'

class UserView1(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename='files/'+form.thumbgen_filename(model.path)))

    column_formatters = {
        'path':_list_thumbnail

    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True),
                                      url_relative_path='files/')
    }

    """
    This class demonstrates the use of 'rules' for controlling the rendering of forms.
    """
    form_create_rules = [
        # Header and four fields. Email field will go above phone field.
        rules.FieldSet(('first_name', 'last_name', 'email', 'phone','path'), 'Personal'),
        # Separate header and few fields
        rules.Header('Location'),
        rules.Field('city'),
        # String is resolved to form field, so there's no need to explicitly use `rules.Field`
        'country',
        # Show macro that's included in the templates
        rules.Container('rule_demo.wrap', rules.Field('notes'))
        #rules.FieldSet('path')
    ]

    # Use same rule set for edit page
    form_edit_rules = form_create_rules

    create_template = 'create_user.html'
    edit_template = 'edit_user.html'
# Flask views

@mod.route('/123')
def index():

	database_path = os.path.join(ROOT_DIR, app.config['DATABASE_FILE'])
	return "{}".format(database_path)
    #return '<a href="/admin/">Click me to get to Admin!</a>'

#@mod.route('/')
#def homepage():
	#return render_template('admin/index.html')
# Create admin
admin = Admin(app, 'Admin: Forms', template_mode='bootstrap2')

# Add views
'''
admin.add_view(FileView(File, db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(UserView1(User1, db.session))
admin.add_view(PageView(Page, db.session))
'''
admin.add_view(FileView(database.File, db.session))
admin.add_view(ImageView(database.Image, db.session))
admin.add_view(UserView(database.Users, db.session))
admin.add_view(ArticlesView(database.Articles, db.session))
admin.add_view(ArticlesView(database.Templates, db.session))
admin.add_view(UserView1(database.User1, db.session))
admin.add_view(PageView(database.Page, db.session))
#admin.add_view(rediscli.RedisCli(Redis()))






if __name__ == '__main__':
	pass

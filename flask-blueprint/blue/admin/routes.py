from flask import Blueprint, render_template

mod = Blueprint('admin', __name__, template_folder='templates',static_folder='static')

@mod.route('/')
def homepage():
	return render_template('admin/index.html')

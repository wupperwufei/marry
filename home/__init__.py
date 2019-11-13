from flask import Blueprint
home = Blueprint('home', __name__ ,static_folder='../static/home',
                 template_folder='../templates/home')
from home import view


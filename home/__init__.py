from flask import Blueprint
home=Blueprint('home',__name__,static_url_path='',static_folder='static/home',
               template_folder='templates/home')
from . import view
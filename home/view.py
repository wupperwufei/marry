from flask import render_template
from . import home

@home.route('/login/<int:name>',methods=["GET", "POST"])
def login(name=None):
    return render_template('login.html',name=name)

@home.route('/reg',methods=["GET", "POST"])
def reg():
    return render_template('reg.html')

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/search/')
def search():
    return render_template('search.html')

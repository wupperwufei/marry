from flask import render_template
from home import home


@home.route('/login/', methods=["GET", "POST"])
def login():
    return render_template('login.html')


@home.route('/reg/', methods=["GET", "POST"])
def reg():
    return render_template('reg.html')


@home.route('/')
def index():
    return render_template('index.html')


@home.route('/search/')
def search():
    return render_template('search.html')

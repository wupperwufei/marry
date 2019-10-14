from flask import render_template
from . import create_app,db
from models import *
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand


app=create_app('default')
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db)

manager.add_command('shell',Shell(make_context=make_shell_context()))
manager.add_command('db',MigrateCommand)
@app.errorhandler(404)
def page_not_found(error):
    return '未找到你的页面'

if __name__ == '__main__':
    app.run(debug=True)

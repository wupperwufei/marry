from flask import render_template
from __init__ import create_app,db
from flask_script import Manager,Shell,Server
from flask_migrate import Migrate,MigrateCommand


app=create_app('default')
manager=Manager(app)
migrate=Migrate(app,db)
# print(app.url_map)
def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('start', Server(host='176.140.8.69', port=9002))
@app.errorhandler(404)
def page_not_found(error):
    return '未找到你的页面'
if __name__ == '__main__':
    manager.run()

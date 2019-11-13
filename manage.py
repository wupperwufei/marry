from flask import render_template
from __init__ import create_app
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from models import *

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


# db.create_all(app=create_app('default'))
# print(app.url_map)
def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('start', Server(host='0.0.0.0', port=9002))


@app.errorhandler(404)
def page_not_found(error):
    return '未找到你的页面'


if __name__ == '__main__':
    manager.run()

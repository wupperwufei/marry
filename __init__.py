from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import  config
db=SQLAlchemy()
def create_app(config_name):
    app=Flask(__name__,static_url_path='/static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    #注册蓝图
    from home import home
    # from admin import admin as admin_blueprint
    app.register_blueprint(blueprint=home)
    # app.register_blueprint(admin_blueprint,url_prefix='/admin')
    return app

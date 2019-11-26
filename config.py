import os


class Config(object):
    SECRET_KEY = 'mrosft'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    '''配置文件初始化'''

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/marry'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:921118@127.0.0.1:3306/marry'
    DEBUG = True


config = {
    'default': DevelopmentConfig
}
config1 = {
        "accountSid": "",  # 主账户id
        "appToken": "",  # 令牌
        "appId": "",  # 应用id
        "templateId": ""  # 模版id
    }
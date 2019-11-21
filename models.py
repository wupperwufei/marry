from __init__ import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 会员号
    iphone = db.Column(db.String(11), unique=True)  # 手机号
    pwd = db.Column(db.String(32))  # 密码
    create_time = db.Column(db.DateTime, default=datetime.now, )  # 注册时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 登录时间
    times = db.Column(db.Integer, default=0)  # 登录次数
    user_info = db.relationship('User_info', backref='user', uselist=False)  # 一对一
    friend = db.relationship('Friend', backref='user', uselist=False)  # 一对一

    def __repr__(self):
        return '<User:%r>' % self.iphone


# 用户信息表
class User_info(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 会员号，外键关联用户表id
    nickname = db.Column(db.String(20))  # 昵称
    image = db.Column(db.String(255))  # 头像
    sex = db.Column(db.Enum('m', 'n'))  # 性别
    birth = db.Column(db.DateTime)  # 出生日期
    age = db.Column(db.String(2))  # 年龄
    high = db.Column(db.String(3), nullable=False)  # 身高
    education = db.Column(db.String(2), nullable=False)  # 学历
    profession = db.Column(db.String(20), nullable=False)  # 职业
    income = db.Column(db.String(1))  # 收入
    property = db.Column(db.String(50), nullable=False)  # 资产
    residence = db.Column(db.String(30), nullable=False)  # 居住地
    register = db.Column(db.String(30), nullable=False)  # 户籍所在地
    qq = db.Column(db.String(20), default='')  # qq
    wechat = db.Column(db.String(30), default='')  # 微信
    email = db.Column(db.String(50), default='')  # 邮箱
    signature = db.Column(db.Text, default='')  # 个性签名
    story = db.relationship('Story', backref='user_info', lazy='dynamic')  # 一对多

    def __repr__(self):
        return '<User_info:%r>' % self.nickname


# 择偶标准
class Friend(db.Model):
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 会员号，外键关联用户表id
    f_age = db.Column(db.String(2), default='')  # 年龄
    f_high = db.Column(db.String(3), default='')  # 身高
    f_education = db.Column(db.String(2), default='')  # 学历
    f_income = db.Column(db.String(1))  # 收入
    f_register = db.Column(db.String(30))  # 户籍
    f_residence = db.Column(db.String(30))  # 居住地


# 婚恋故事
class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)  # 标题
    desc = db.Column(db.String(100), nullable=False)  # 文章描述
    content = db.Column(db.Text, nullable=False)  # 内容
    author = db.Column(db.Integer, db.ForeignKey('user_info.id'))  # 作者，外键关联用户表信息表id
    image = db.Column(db.String(255))  # 图片路径
    created_time = db.Column(db.DateTime, default=datetime.now)  # 发布时间
    times = db.Column(db.String(20), default=0)  # 浏览次数


# 婚恋课堂
class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)  # 视频id
    title = db.Column(db.String(30), nullable=False)  # 标题
    video = db.Column(db.String(100), nullable=False)  # 视频资源路径
    image = db.Column(db.String(100), nullable=False)  # 封面图片路径
    desc = db.Column(db.String(100), nullable=False)  # 描述
    times = db.Column(db.String(20), default=0)  # 点击量

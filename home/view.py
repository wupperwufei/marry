import hashlib
import os

from flask import render_template, request, make_response, Response, redirect, jsonify
from werkzeug.utils import secure_filename

from home import home
from models import User, db, User_info, Friend

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@home.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        uphone = request.form.get('uphone')
        upass = request.form.get('upass')
        user = User.query.filter_by(iphone=uphone).first()
        if not user:
            print('%s用户名错误' % uphone)
            return jsonify1({'status': 0, 'mes': '用户名或密码错误'})
        elif user.pwd != md5(upass):
            print('%s密码错误' % uphone)
            return jsonify1({'status': 0, 'mes': '用户名或密码错误'})
        res = redirect('/immed/')
        res.set_cookie('name', uphone, 60 * 60 * 24)
        res.set_cookie('id', str(user.id), 60 * 60 * 24)
        return res


@home.route('/reg/', methods=["GET", "POST"])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    else:
        uphone = request.form.get('uphone')
        upass = request.form.get('upass')
        upass1 = request.form.get('upass1')
        if upass != upass1:
            return Response('两次密码不一致')
        if not upass:
            return Response('密码不能为空')
        try:
            user = User(iphone=uphone, pwd=md5(upass))
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            print('不能重复注册')
            return Response('不能重复注册')
        return redirect('/login/')


@home.route('/')
def index():
    is_login = request.cookies.get('name')
    return render_template('index.html', is_login=is_login)


@home.route('/search/')
def search():
    is_login = request.cookies.get('name')
    return render_template('search.html', is_login=is_login)


@home.route('/findpassword/')
def findpwd():
    is_login = request.cookies.get('name')
    return render_template('findpassword.html')


@home.route('/check_phone/')
def check_phone():
    uphone = request.args.get('uphone')
    user = User.query.filter_by(iphone=uphone).first()
    if user:
        data = {'status': 0, 'mes': 'NO'}
    else:
        data = {'status': 1, 'mes': 'OK'}
    print(data)
    return jsonify1(data)


@home.route('/logout/')
def logout():
    res = redirect('/')
    res.delete_cookie('name')
    res.delete_cookie('id')
    return res


@home.route('/immed/', methods=["GET", "POST"])
def immed():
    if request.method == 'GET':
        is_login = request.cookies.get('name')
        if not is_login:
            print('未登录')
            return redirect('/login/')
        else:
            return render_template('immed.html',is_login=is_login)
    else:
        print(request.form)
        id = request.cookies.get('id')
        nickname = request.form.get('nickname')
        sex = request.form.get('sex')
        birth = request.form.get('birth')
        age = request.values.get("age")
        high = request.form.get('high')
        image1 = request.files.get('image')
        filename = secure_filename(image1.filename)
        img=filename
        image1.save(os.path.join(BASE_DIR + '/static/home/media', filename))
        education = request.form.get('education')
        profession = request.form.get('profession')
        property = request.form.get('property')
        income = request.form.get('income')
        residence = request.form.get('residence')
        register = request.form.get('register')
        qq = request.form.get('qq')
        wechat = request.form.get('wechat')
        email = request.form.get('email')
        f_age = request.form.get('f_age')
        f_high = request.form.get('f_high')
        f_income = request.form.get('f_income')
        f_education = request.form.get('f_education')
        f_register = request.form.get('f_register')
        f_residence = request.form.get('f_residence')
        try:
            user_info = User_info(user_id=id, nickname=nickname, image=img,
                                  sex=sex, birth=birth, age=age, high=high, education=education,
                                  profession=profession, income=income, property=property,
                                  residence=residence, register=register, qq=qq, wechat=wechat,
                                  email=email)
            friend = Friend(user_id=id, f_age=f_age, f_high=f_high, f_education=f_education,
                            f_income=f_income, f_register=f_register, f_residence=f_residence,
                            )
            db.session.add(user_info)
            db.session.add(friend)
            db.session.commit()
        except Exception as e:
            print(e)
            return Response('用户信息提交失败')
        return redirect('/')


def md5(data):
    data = data.encode()
    a = hashlib.md5()
    a.update(data)
    data = a.hexdigest()
    return data


def jsonify1(dct):
    import json
    return json.dumps(dct, ensure_ascii=False)

import hashlib
import json
import os
import random

from sms import YunTongXin
from config import config1
from flask import render_template, request, Response, redirect, jsonify, session
from werkzeug.utils import secure_filename
from sqlalchemy import extract
from home import home
from models import User, db, User_info, Friend

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@home.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        if 'name' in session:
            is_login = session.get('name')
            return render_template('index.html', is_login=is_login)
        if request.cookies.get('name'):
            is_login = request.cookies.get('name')
            session['name'] = request.cookies.get('name')
            return render_template('index.html', is_login=is_login)
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
        if user.times == 0:
            res = redirect('/immed/')
        else:
            res = redirect('/')
        update_row = 'update user set times=times+1 where iphone=%s' % (uphone)
        db.session.execute(update_row)
        db.session.commit()
        session['name'] = uphone
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
    # is_login = request.cookies.get('name')
    is_login = session.get('name')
    return render_template('index.html', is_login=is_login)


@home.route('/search/',methods=["GET", "POST"])
def search():
    #判断是否用户是否登录,登录则显示用户名
    is_login = session.get('name')
    user_new = User.query.order_by(User.update_time.desc())
    new_list = []
    for i in range(2):
        new_user = User_info.query.filter_by(user_id=user_new[i].id).first()
        new_list.append(new_user)

    """
    搜索功能
    """
    try:
        if request.method == 'GET':
            page = int(request.args.get('page',1))
            user_list = User.query.order_by(User.create_time.desc()).paginate(page=page,per_page=2)

            page_data = []
            for i in user_list.items:
                data = User_info.query.filter_by(user_id=i.id).first()
                page_data.append(data)

            return render_template("search.html", page_data=page_data,paginate=user_list,new_list=new_list,is_login=is_login)

        elif request.method == 'POST':
            #获取json数据并解析
            data = json.loads(request.form.get('data',''))
            op_text = data['option']
            op_gender = data['op_gender']
            op_birth = data['op_birth']
            page = data['page']
            order = data['order']
            print(op_text)
            print(op_gender)
            print(op_birth)
            print(page)
            print(order)

            #对性别字符进行处理
            if op_gender == '男朋友':
                op_gender = 'M'
            else:
                op_gender = 'F'

            #判断是否需要进行特定的排序
            if order == 0:  #不需要对特定的字段进行排序显示
                #筛选数据库中符合的用户的信息，并进行分页
                option_user = User_info.query.filter(User_info.nickname.like("%" + op_text + "%") if op_text is not None else "",extract('year', User_info.birth)== op_birth,User_info.sex==op_gender).paginate(page=page, per_page=2)
                print(option_user.items)

                if option_user:
                    opt_list = []
                    # 按照最新登录时间进行顺序匹配
                    for u in user_new:
                        for user in option_user.items:
                            if user.user_id == u.id:
                                opt_list.append(user)
                    print(opt_list)
                    # 总页数
                    total = option_user.total
                    print(total)

                    page_data = Ajax_send(opt_list,total,page,order)
                    return jsonify({'code': 200, 'data': page_data})
                else:
                    return jsonify({'code': 10008, 'data': {'error': "未查到相关用户"}})
            elif order in range(1,4):
                if order == 1:  #需要进行高度降序排列
                    option_user = User_info.query.filter(User_info.nickname.like("%" + op_text + "%"),extract('year',User_info.birth) == op_birth, User_info.sex == op_gender).order_by(User_info.high.desc()).paginate(page=page,per_page=2)
                    print(option_user.items)
                    if option_user:
                        # 总页数
                        total = option_user.total
                        print(total)

                        page_data = Ajax_send(option_user.items, total, page, order)
                        return jsonify({'code': 200, 'data': page_data})

                    else:
                        return jsonify({'code': 10008, 'data': {'error': "未查到相关用户"}})

                elif order == 2:  #需要进行高度降序排列
                    option_user = User_info.query.filter(User_info.nickname.like("%" + op_text + "%"),extract('year',User_info.birth) == op_birth, User_info.sex == op_gender).order_by(User_info.property.desc).paginate(page=page,per_page=2)
                    print(option_user.items)
                    if option_user:
                        # 总页数
                        total = option_user.total
                        print(total)

                        page_data = Ajax_send(option_user.items, total, page, order)
                        return jsonify({'code': 200, 'data': page_data})

                    else:
                        return jsonify({'code': 10008, 'data': {'error': "未查到相关用户"}})

                elif order == 3:  #需要进行高度降序排列
                    option_user = User_info.query.filter(User_info.nickname.like("%" + op_text + "%"),extract('year', User_info.birth) == op_birth,User_info.sex == op_gender).paginate(page=page, per_page=2)
                    user = User.query.order_by(User.times.desc)
                    if option_user:
                        opt_list = []
                        for u in user:
                            for user in option_user.items:
                                if user.user_id == u.id:
                                    opt_list.append(user)
                        print(opt_list)
                        # 总页数
                        total = option_user.total
                        print(total)

                        page_data = Ajax_send(opt_list, total, page, order)
                        return jsonify({'code': 200, 'data': page_data})
                    else:
                        return jsonify({'code': 10008, 'data': {'error': "未查到相关用户"}})
            else:
                return jsonify({'code': 10009, 'data': {'error': "操作出错,请重试"}})
    except Exception as e:
        print('fail', e)
        return render_template("search.html")

def Ajax_send(opt_list,total,page,order):
    # 遍历出来所有选择的用户信息，发送给前端
    page_data = []
    for i in opt_list:
        d = {}
        d['image'] = i.image
        d['nickname'] = i.nickname
        d['age'] = i.age
        d['education'] = i.education
        d['high'] = i.high
        d['profession'] = i.profession
        d['property'] = i.property
        d['total'] = total
        d['page'] = page
        d['order'] = order
        page_data.append(d)
    print(page_data)
    return page_data

@home.route('/findpassword/')
def findpwd():
    if request.method == 'GET':
        return render_template('findpassword.html')
    else:
        iphone = request.form.get('uphone')
        yzm = request.form.get('code')
        if session.get(iphone) == yzm:
            return redirect('/updatepassword/')
        else:
            print('验证码错误')
            return render_template('findpassword')


@home.route('/updatepassword/')
def updatepwd():
    if request.method == 'GET':
        return render_template('updatepassword.html')
    else:
        upass = request.form.get('upass')
        upass1 = request.form.get('upass1l')
        id = session.get('name')
        if upass != upass1:
            print('两次密码不一致')
            return jsonify1({'status': 10010, 'mes': '密码填写错误'})
        user = User.query.filter_by(id=id).first()
        user.pwd = upass
        db.session.add(user)
        db.session.commit()
        return redirect('/login/')


# 发送验证码短信
@home.route('/get_yzm/')
def get_yzm():
    iphone = request.form.get('uphone')
    code = random.randint(1000, 10000)  # 产生4位验证码
    yun = YunTongXin(**config1)
    res = yun.run(iphone, code)
    print(res)
    if res.statusCode == 200:
        session[iphone] = code
    res1 = {'status': res.statusCode, 'mes': res.statusMsg}
    return jsonify1(res1)


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
    del session['name']
    if request.cookies.get('name'):
        res.delete_cookie('name')
    if request.cookies.get('id'):
        res.delete_cookie('id')
    return res


@home.route('/immed/', methods=["GET", "POST"])
def immed():
    if request.method == 'GET':
        # is_login = request.cookies.get('name')
        is_login = session.get('name')
        if not is_login:
            print('未登录')
            return redirect('/login/')
        else:
            return render_template('immed.html', is_login=is_login)
    else:
        print(request.form)
        # id = request.cookies.get('id')
        id = session.get('name')
        user = User.query.filter_by(iphone=id).first()
        nickname = request.form.get('nickname')
        sex = request.form.get('sex')
        birth = request.form.get('birth')
        age = request.values.get("age")
        high = request.form.get('high')
        image1 = request.files.get('image')
        filename = secure_filename(image1.filename)
        img = filename
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
            user_info = User_info(user_id=user.id, nickname=nickname, image=img,
                                  sex=sex, birth=birth, age=age, high=high, education=education,
                                  profession=profession, income=income, property=property,
                                  residence=residence, register=register, qq=qq, wechat=wechat,
                                  email=email)
            friend = Friend(user_id=user.id, f_age=f_age, f_high=f_high, f_education=f_education,
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

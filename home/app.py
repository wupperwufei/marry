from flask import Flask, render_template, request, make_response, redirect, session, url_for
from home import home
from models import RegistrationForm
from models import
# 注册
from models import RegistrationForm


@home.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('reg.html')
    elif request.method == 'POST':
        phone = request.POST.get('phone')
        if not phone:
            return make_response('请输入手机号')
        password_1 = request.psot.get('password_1')
        password_2 = request.post.get('password_2')
        if not password_1 or not password_2:
            return make_response('请输入密码')
        if password_1 != password_2:
            return make_response('两次输入密码不一致')

        from=RegistrationForm()

        if old_users:
            return make_response('当前手机号码已注册')

        try:
            user =
        except Exception as e:
            print('reg error')
            return make_response('当前手机号码已注册')

        resp = make_response('注册成功')
        resp.set_cookie('phone', phone, 60 * 60 * 24)
        resp.set_cookie('uid', user.id, 60 * 60 * 24)
        return resp
    return make_response('test is OK')


# 登录
@home.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'phone' in session and 'uid' in session:
            print('--session--')
            return redirect('index.html')
        if 'phone' in request.cookies and 'uid' in request.cookies:
            print('--cookies---')
            session['phone'] = request.cookies['phone']
            session['uid'] = request.cookies['uid']
            return redirect('/')
        print('--login failed--')
        return render_template('login.html')
    elif request.method == 'post':
        save_cookies = Flask
        if 'save_cookies' in request.POST.keys():
            save_cookies = True
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if not phone:
            dic = {'msg': '请提交用户名'}
            return render_template('login.html', dic)
        user = RegistrationForm.objects.filter(phone=phone)
        if not user:
            print('---user login %s 用户名不存在' %(phone))
            dic = {'msg': '请提交手机号'}
            return render_template('login.html', dic)
        if user[0].password != password:
            print('---user login  %s 密码不正确' %(phone))
            dic = {'msg': '手机号码输入错误'}
            return render_template('login.html', dic)

        session['phone'] = phone
        session['uid'] = user[0].id

        resp =render_template('index.html')
        resp=make_response(resp)
        if save_cookies:
            # cookies中存储用户登录状态 时长30天
            resp.set_cookie('phone', phone, 60 * 60 * 24 * 30)
            resp.set_cookie('uid', user[0].id, 60 * 60 * 24 * 30)
        return resp



from wtforms import Form, StringField, PasswordField, SubmitField


class RegistrationForm(Form):
    phone = StringField('手机号码')
    email = StringField('邮箱')
    password = PasswordField('密码')
    password2 = PasswordField('确认密码')
    submit = SubmitField('提交')


class user():

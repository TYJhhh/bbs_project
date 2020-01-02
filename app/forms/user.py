from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email
class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,30,message="用户名长度不符合要求")])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,30,message="密码长度不符合要求")])
    confirm  = PasswordField('确认密码',validators=[EqualTo('password',message="两次密码不一致")])
    email = StringField('邮箱',validators=[Email(message="邮箱格式不正确")])
    submit = SubmitField("立即注册")

class LoginForm():
    pass
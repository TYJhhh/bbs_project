from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import photos
from app.models import User
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 30, message="用户名长度不符合要求")])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 30, message="密码长度不符合要求")])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message="两次密码不一致")])
    email = StringField('邮箱', validators=[Email(message="邮箱格式不正确")])
    submit = SubmitField("立即注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 30, message="用户名长度不符合要求")])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 30, message="密码长度不符合要求")])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

# 头像上传表单
class UploadedForm(FlaskForm):
    icon = FileField('头像', validators=[FileRequired('请选择头像'), FileAllowed(photos, FileAllowed(photos, message='只能上传图片'))])
    submit = SubmitField('立即上传')
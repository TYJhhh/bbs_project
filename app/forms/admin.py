from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class AdminForm(FlaskForm):
    username = StringField('管理员', validators=[DataRequired(), Length(5, 15, message="用户名长度不符合要求")])
    password = PasswordField('密码', validators=[DataRequired(), Length(5, 15, message="密码长度不符合要求")])
    submit = SubmitField('登录')
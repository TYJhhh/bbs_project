from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import RegisterForm
from app.models import User
from app.extensions import db
from app.email import send_mail

user = Blueprint('user', __name__)


@user.route('/', methods=['GET', 'POST'])
def index():
    # GET请求 为了 让用户看到 战士的界面
    return '我是个人中心页面'

    # post请求为了提交数据


# 注册
# 定制注册页面
# 表单 表单验证
# token安全机制

# 登录
# flask_login 处理登录的逻辑
@user.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # 判断表单输入数据是否符合要求
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(u)
        db.session.commit()

        # 调用模型中生成token的方法
        token = u.generate_active_token()

        # 发送邮件  如果发送成功
        send_mail(u.email, '账户激活', 'email/active', username=u.username, token=token)

        # 告诉用户发送成功 点击链接激活用户
        flash("邮件发送成功 点击链接激活用户")

        # 跳转到 首页 进行登录
        # return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>/')
def activate(token):
    if User.check_active_token(token):
        flash("账户激活成功")
        return redirect(url_for('main.index'))
    else:
        flash("账户激活失败")
        return redirect(url_for('user.register'))

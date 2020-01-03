from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import RegisterForm, LoginForm
from app.models import User
from app.extensions import db
from app.email import send_mail
from flask_login import login_user, logout_user

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


@user.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        u = User.query.filter_by(username=username).first()
        if not u:
            flash("用户名不存在")
        elif not u.confirmed:
            flash("请先激活该用户")
        elif u.verify_password(password=password):
            login_user(u, remember=remember)
            flash("登录成功")
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash("密码无效")
    return render_template('user/login.html', form=form)


@user.route('/logout/')
def logout():
    logout_user()
    flash("退出成功")
    return redirect(url_for('main.index'))
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from app.forms import RegisterForm, LoginForm, UploadedForm
from app.models import User
from app.extensions import db, photos
from app.email import send_mail
from flask_login import login_user, logout_user, current_user
from PIL import Image

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
        return redirect(url_for('user.login'))
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


@user.route('/change_icon/', methods=['POST', 'GET'])
def change_icon():
    form = UploadedForm()
    if form.validate_on_submit():
        # 为了不造成上传图片 重名导致图片替换的问题 需要生产随机文件名
        suffix = os.path.splitext(form.icon.data.filename)[1]
        filename = random_string() + suffix
        photos.save(form.icon.data, name=filename)

        # 生成缩略图
        # 告诉类库 要处理哪里的图片
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        image = Image.open(pathname)
        image.thumbnail((128, 128))
        image.save(pathname)

        # 更新头像
        # 如果用户的头像不是default.jpg 说明用户已经上传过头像了
        # 每个人只能保存除了default.jpg之外的一张头像
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))

        # 然后把上传以后的 裁剪后 的 保存到数据库中
        current_user.icon = filename    # 通过更新属性的值来更新数据库
        db.session.add(current_user)    # 更新当前用户的信息
        flash("头像已保存")
        return redirect(url_for('user.change_icon'))
    img_url = photos.url(current_user.icon) # 获取上传图片的地址 用于显示
    return render_template('user/change_icon.html', form=form, img_url=img_url)

def random_string(length=32):
    import random
    base_string = 'qwertyuiopasdfghjklzxcvbnm0123456789'
    return "".join(random.choice(base_string) for i in range(length))
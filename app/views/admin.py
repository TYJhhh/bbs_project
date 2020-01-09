from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User, Posts, Comment, Admin
from app.forms import AdminForm
from app.extensions import db

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET', 'POST'])
def index():
    form = AdminForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        a = Admin.query.filter_by(username=username).first()
        if not a:
            flash("管理员账号错误")
        elif a.verify_password(password=password):
            flash("登录成功")
            return redirect(url_for('admin.manage_users', uname=a.username))
        else:
            flash("密码错误")
    return render_template('admin/manage_login.html', form=form)


@admin.route('/manage_users/<uname>', methods=['GET', 'POST'])
def manage_users(uname):
    ad = Admin.query.filter_by(username=uname).first()
    if not ad:
        flash("请先登录")
        return redirect(url_for('admin.index'))
    page = request.args.get('page', 1, type=int)  # 用户想查看第几页
    pagination = User.query.filter_by().order_by(User.id.asc()).paginate(page, per_page=10, error_out=False)
    users = pagination.items
    return render_template('admin/manage_users.html', uname=uname, pagination=pagination, users=users)


@admin.route('/manage_posts/<uname>', methods=['GET', 'POST'])
def manage_posts(uname):
    ad = Admin.query.filter_by(username=uname).first()
    if not ad:
        flash("请先登录")
        return redirect(url_for('admin.index'))
    page = request.args.get('page', 1, type=int)  # 用户想查看第几页
    pagination = Posts.query.filter_by().order_by(Posts.id.asc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('admin/manage_posts.html', uname=uname, pagination=pagination, posts=posts)


@admin.route('/manage_comments/<uname>', methods=['GET', 'POST'])
def manage_comments(uname):
    ad = Admin.query.filter_by(username=uname).first()
    if not ad:
        flash("请先登录")
        return redirect(url_for('admin.index'))
    page = request.args.get('page', 1, type=int)  # 用户想查看第几页
    pagination = Comment.query.filter_by().order_by(Comment.id.asc()).paginate(page, per_page=10, error_out=False)
    comments = pagination.items
    return render_template('admin/manage_comments.html', uname=uname, pagination=pagination, comments=comments)

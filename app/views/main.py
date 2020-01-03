from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import PostsForm
from flask_login import current_user
from app.models import Posts
from app.extensions import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    # GET请求为了让用户看到展示的界面
    form = PostsForm()
    if form.validate_on_submit():
        # 判断用户是否登录
        if current_user.is_authenticated:
            # 获取当前的登录用户
            u = current_user._get_current_object()
            p = Posts(content=form.content.data, user=u)
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash("请先登录")
            return redirect(url_for('user.login'))
    # posts = Posts.query.filter_by(rid=0).all()
    page = request.args.get('page', 1, type=int)  # 用户想查看第几页
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)

    # POST请求为了提交数据
from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user
from app.models import User, Posts, Comment
from app.forms import PostsForm, CommentForm
from app.extensions import db
import re

posts = Blueprint('posts', __name__)


@posts.route('/', methods=['GET', 'POST'])
def index():
    # GET请求为了让用户看到展示的界面
    form = PostsForm()
    if form.validate_on_submit():
        # 获取当前的登录用户
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u)
        db.session.add(p)
        db.session.commit()
        if p.body_html:  # /<\.+?>/g
            p_re = r'<\/?.+?>'
            re.compile(p_re)
            p.body_text = re.sub(p_re, "", p.body_html)
        return redirect(url_for('main.index'))
    return render_template('posts/post_edit.html', form=form)

    # POST请求为了提交数据


@posts.route('/posts/<int:pid>')
def collect(pid):
    if current_user.is_favorite(pid):
        # 取消收藏
        current_user.del_favorite(pid)
        post = Posts.query.get(pid)
        post.rid -= 1
        db.session.commit()
    else:
        current_user.add_favorite(pid)
        post = Posts.query.get(pid)
        post.rid += 1
        db.session.commit()
    return jsonify({'code': 'OK'})

@posts.route('/post_show/<int:id>/', methods=['GET', 'POST'])
def post_show(id):
    post = Posts.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, user=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('评论成功')
        return redirect(url_for('posts.post_show', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)  # 用户想查看第几页
    if page == -1:
        page = (post.comments.count() - 1) // 6 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=6, error_out=False)
    comments = pagination.items
    return render_template('posts/post_show.html', post=post, form=form, comments=comments, pagination=pagination, count=post.comments.count(), fav_count=post.rid)

@posts.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Posts.query.get_or_404(id)
    form = PostsForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        if post.body_html:  # /<\.+?>/g
            p_re = r'<\/?.+?>'
            re.compile(p_re)
            post.body_text = re.sub(p_re, "", post.body_html)
        flash("操作成功")
        return redirect(url_for('posts.post_show', id=post.id, post=post))
    form.content.data = post.content
    return render_template('posts/post_edit.html', form=form, modify_code=159)

@posts.route('/del_comment/<int:id>')
def del_comment(id):
    commemt = Comment.query.get_or_404(id)
    db.session.delete(commemt)
    db.session.commit()
    flash("删除成功")
    return redirect(url_for('posts.post_show', id=commemt.post_id))
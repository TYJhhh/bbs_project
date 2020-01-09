from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.models import Posts
import hotSearch

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    # GET请求为了让用户看到展示的界面
    # posts = Posts.query.filter_by(rid=0).all()
    page = request.args.get('page', 1, type=int)  # 用户想查看第几页
    pagination = Posts.query.filter_by().order_by(Posts.timestamp.desc()).paginate(page, per_page=6, error_out=False)
    posts = pagination.items
    rank = hotSearch.main()
    # for post in posts:
    #     if post.body_html:  # /<\.+?>/g
    #         p = r'<\/?.+?>'
    #         re.compile(p)
    #         post.body_text = re.sub(p, "", post.body_html)
    return render_template('main/index.html', posts=posts, pagination=pagination, rank=rank)

    # POST请求为了提交数据
# p = r'<\/?.+?>'
# import re
# pattren = re.compile(p)
# re.sub(p, "", "<h1>132</h1>")
# '132'
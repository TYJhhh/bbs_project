from flask import Blueprint, jsonify
from flask_login import current_user

posts = Blueprint('posts', __name__)


@posts.route('/', methods=['GET', 'POST'])
def index():
    # GET请求为了让用户看到展示的界面
    return '我是文章发表页面'

    # POST请求为了提交数据


@posts.route('/posts/<int:pid>')
def collect(pid):
    if current_user.is_favorite(pid):
        # 取消收藏
        current_user.del_favorite(pid)
    else:
        current_user.add_favorite(pid)
    return jsonify({'code': 'OK'})

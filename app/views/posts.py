from flask import Blueprint

posts = Blueprint('posts', __name__)

@posts.route('/', methods=['GET', 'POST'])
def index():
    # GET请求为了让用户看到展示的界面
    return '我是文章发表页面'

    # POST请求为了提交数据
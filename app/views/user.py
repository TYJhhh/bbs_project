from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/', methods=['GET', 'POST'])
def index():
    # GET请求为了让用户看到展示的界面
    return '我是个人中心页面'

    # POST请求为了提交数据
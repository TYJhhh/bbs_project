from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    # GET请求为了让用户看到展示的界面
    return '我是主页'

    # POST请求为了提交数据
from .main import main
from .user import user
from .posts import posts
from .admin import admin

# 配置蓝本
DEFAULT_BLUEPRINT = (
    (main, ''),
    (user, '/user'),
    (posts, '/posts'),
    (admin, '/admin')
)

# 注册蓝本 封装成函数
def config_blueprint(app):
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

# 一个目录的入口  方便 其它目录导入
from flask import Flask
from app.views import config_blueprint
from app.config import config
from app.extensions import config_extensions

# 封装一个函数 专门用来 创建app实例
def create_app(config_name): # config_name development test product
    app = Flask(__name__, static_url_path="")
    app.config.from_object(config[config_name])  # 此时你是开发还是测试还是生产
    config[config_name].init_app(app)  # 让配置文件生效
    config_blueprint(app)
    config_extensions(app)
    return app
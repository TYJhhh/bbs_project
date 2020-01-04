import os

# 后期我们想上传文件 或者说 保存 sqlite数据库文件 那么我们需要设置目录

base_dir = os.path.abspath(os.path.dirname(__file__))   # 这个就是app的目录
# class Person(object):
#     def __init__(self, username, password, age):
#         self.username = username
#         self.password = password
#         self.age = age
# person = Person()       # 对应数据表的名字
# person.username = 'zhangsan'  # username就是数据字段的名字
#                               # zhangsan就是数据行

# 通用配置
class Config:
    # 数据库的操作
    # orm 对象关系映射模型
    #
    SECRET_KEY = 'AFDADF122121ASADF'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'     # 邮件服务器地址
    MAIL_USERNAME = '1227794413@qq.com'    # 邮件账户名
    MAIL_PASSWORD = 'ekdevueqmiwshhhf'     # 邮件账户授权码

    # 文件上传的配置信息
    MAX_CONTENT_LENGTH = 8*1024*1024    # 上传文件的大小
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/uploads')

    # 加载本地bootstrap静态文件
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass

# 开发环境数据库
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'bbs_dev.sqlite')

# 测试环境数据库
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'bbs_test.sqlite')

# 生产环境数据库
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'bbs_production.sqlite')

config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'product': ProductionConfig,
    'default': DevelopmentConfig
}
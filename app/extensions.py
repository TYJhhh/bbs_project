from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads, patch_request_class
# 实例化对象

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate(db=db) # 需要跟app 绑定 并且还要告诉他你要往哪里迁移
loginmanager = LoginManager()
moment = Moment()
photos = UploadSet('photos', IMAGES)    # 只能上传图片

# 跟app完成绑定
def config_extensions(app):
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    loginmanager.init_app(app)
    moment.init_app(app)

    # 指定登录的登录地址
    loginmanager.login_view = 'user.login'
    # 登陆的提示信息
    loginmanager.login_message = '只有登录才能访问'
    # session的保护级别  basic   strong
    loginmanager.session_protection = 'strong'

    configure_uploads(app, photos)  # 将上传对象跟app绑定
    patch_request_class(app, size=None)  # 如果为None 就以我们自己设置的为准
    # 否则就是默认的64M
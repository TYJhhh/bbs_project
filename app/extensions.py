from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate

# 实例化对象

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()

# 跟app完成绑定
def config_extensions(app):
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
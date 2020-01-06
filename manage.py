from flask_script import Manager
from app.models import User, Posts
from flask_migrate import MigrateCommand
from app import create_app
from app.extensions import db

app = create_app('default')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# python manage.py  runserver -d -r -p 5005 -h 0.0.0.0 --threaded
# python  manage.py db init  初始化迁移目录
# python  manage.py db migrate  生成迁移脚本
# python  manage.py db upgrade  映射到数据库中

@manager.command
def create_test_posts():
    for x in range(1, 100):
        content = '内容: %s' % x
        user = User.query.first()
        p = Posts(content=content, user=user)
        db.session.add(p)
        db.session.commit()
    print("添加测试数据成功")

if __name__ == "__main__":
    manager.run()
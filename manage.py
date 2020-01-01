from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app

app = create_app('default')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# python  manage.py db init  初始化迁移目录
# python  manage.py db migrate  生成迁移脚本
# python  manage.py db upgrade  映射到数据库中

if __name__ == "__main__":
    manager.run()
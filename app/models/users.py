from app.extensions import db, loginmanager
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
#                                     加密             解密
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(64), default='default.jpg')

    # 添加关联模型    我们后期想知道这个文章是谁发表的
    # 这个作者发表了哪些文章
    posts = db.relationship('Posts', backref='user', lazy='dynamic')

    # 1密码用户返回
    # 2不能读密码
    @property
    def password(self):
        raise AttributeError('密码不可读')

    # 保存加密后的密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    # 密码校验 正确返回 true  否则返回false
    # 用户输入没有加密的密码 收到以后先加密 然后再跟数据库中的进行比较
    # 如果通过就说明密码正确

    def verify_password(self, password):
        # self.password_hash 数据库中的
        # password 用户输入的
        return check_password_hash(self.password_hash, password)

    # 生成激活账户的token   #expires_in表示过期时间
    def generate_active_token(self, expires_in=3600):
        # current_app 当前app的实例
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    # 检测token是否是合法并且是否过期
    def check_active_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        # 解密token 如果符合要求 拿出 token中的 id  知道是哪个用户
        # 被激活  根据token中的id 拿到用户的信息
        u = User.query.get(data.get('id'))

        if not u:
            return False
        if not u.confirmed:
            u.confirmed = True
            db.session.add(u)  # 将数据库中的字段 激活
        return True

# 登录认证的 一个回调函数  也就是要告诉服务器到底是谁登录了
# 退出登录 也需要知道该删除谁的session
@loginmanager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))
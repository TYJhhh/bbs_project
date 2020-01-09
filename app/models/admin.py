from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

from app.extensions import db
from flask_login import UserMixin
class User(UserMixin,db.model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
    icon = db.Column(db.String(64),default='default.jpg')
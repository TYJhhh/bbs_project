from app.extensions import db
from datetime import datetime
from markdown import markdown
import bleach

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 添加外键  '表名.字段'
    uid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    # favorites = db.relationship('User', secondary="collections", backref=db.backref('post', lazy='dynamic'),
    #                             lazy='dynamic')

    body_html = db.Column(db.Text)
    body_text = db.Column(db.Text)
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))

db.event.listen(Posts.content, 'set', Posts.on_changed_body)
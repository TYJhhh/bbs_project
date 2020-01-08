from .users import User
from .posts import Posts
from .comments import Comment
from app.extensions import db

# 用户帖子的中间表  主键  用户的id   帖子的id
# 因为 一个用户可以收藏多篇文章   一篇文章可以被多个用户收藏   多对多
collections = db.Table("collections",
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))
)

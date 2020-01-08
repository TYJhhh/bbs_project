from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_pagedown.fields import PageDownField

class PostsForm(FlaskForm):
    content = PageDownField("博客发表", render_kw={'placeholder': '你想记录...'}, validators=[DataRequired()])
    submit = SubmitField("发表")

class CommentForm(FlaskForm):
    body = TextAreaField("评论", render_kw={'placeholder': '这一刻你想说...'}, validators=[DataRequired()])
    submit = SubmitField('发表')
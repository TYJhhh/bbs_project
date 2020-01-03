from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length

class PostsForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '这一刻你想说...'}, validators=[Length(10, 200, message="字数不符")])
    submit = SubmitField("发表")
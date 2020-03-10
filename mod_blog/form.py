from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from Utils.forms import MultipleCheckboxField


class PostForm(FlaskForm):
    title = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    categories = MultipleCheckboxField()


class CategoryForm(FlaskForm):
    name = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    description = TextAreaField()

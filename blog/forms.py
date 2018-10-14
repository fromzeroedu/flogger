from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from blog.models import Category

def categories():
    return Category.query

class PostForm(FlaskForm):
    title = StringField('Title', [
            validators.InputRequired(),
            validators.Length(max=80)
        ])
    body = TextAreaField('Content', validators=[validators.InputRequired()])
    category = QuerySelectField('Category', query_factory=categories,
        allow_blank=True)
    new_category = StringField('New Category')
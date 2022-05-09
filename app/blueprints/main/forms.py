from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from ...models import User
from jinja2.utils import markupsafe


class PokedexForm(FlaskForm):
    pokename = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
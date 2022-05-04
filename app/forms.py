from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# FORM SECTION
class PokedexForm(FlaskForm):
    pokename = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
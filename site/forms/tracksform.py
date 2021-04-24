from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired


class TracksForm(FlaskForm):
    name = StringField('Track Title', validators=[DataRequired()])
    genreid = SelectField('Genre')
    albumid = SelectField('Album')
    seconds = IntegerField('Duration')
    submit = SubmitField('Submit')

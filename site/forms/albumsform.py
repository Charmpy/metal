from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class AlbumsForm(FlaskForm):
    title = StringField('Album Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    artistid = SelectField('Artist')

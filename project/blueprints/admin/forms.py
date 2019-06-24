from wtforms import TextAreaField, SubmitField, StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm


class SearchBox(FlaskForm):
    identity = StringField('',
                           [DataRequired(), Length(3, 254)])

from wtforms import TextAreaField, SubmitField, StringField, PasswordField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm


class TopicForm(FlaskForm):
    topic = StringField('Topic',[DataRequired(), Length(1, 25)])

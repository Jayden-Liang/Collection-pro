from wtforms import TextAreaField, SubmitField, StringField, PasswordField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RecipeForm(FlaskForm):
    title = StringField(validators=[
      Length(3, 68),
      DataRequired()
    ])
    category = SelectField('选择分类', choices=[('east', '中餐'), ('west', '西餐')])
    ingredients =  StringField(validators=[Length(3, 290), DataRequired()])
    steps = TextAreaField(validators=[
      Length(3,500),
      DataRequired()
    ])
    photo = FileField(u'上传图片', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'])])

# class UploadForm(FlaskForm):

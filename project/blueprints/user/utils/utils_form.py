from wtforms.validators import ValidationError
from project.blueprints.user.models import User

def check_exist(message=None):
    if message is None:
        message = '邮箱或名字已存在'
    def check(form, field):
        if User.find_by_identity(field.data):
            raise ValidationError(message)
    return check

def check_email(form, field):
    if not User.find_by_identity(field.data):
        raise ValidationError('邮箱未注册')

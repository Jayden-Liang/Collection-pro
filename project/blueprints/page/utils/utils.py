import random
from project.blueprints.user.models import User, Role, Blog, Topic, Todo
from flask_login import current_user
from sqlalchemy import and_

# 辅助函数
def get_random_study():
    if current_user.is_anonymous:
        blogs= User.query.filter_by(email='liangjisong@foxmail.com').first().blogs
    else:
        blogs =current_user.blogs
    if blogs ==[]:
        return None
    index = random.randint(0,len(blogs)-1)
    random_today  = blogs[index]
    return random_today

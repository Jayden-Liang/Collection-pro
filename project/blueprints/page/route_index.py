from flask import Blueprint, render_template
from flask_login import login_required
from project.blueprints.user.models import User, Role, Blog, Topic, Todo
import random

page = Blueprint('page', __name__, template_folder='templates')

def get_random_study():
    last_id = Blog.query.filter().order_by(Blog.id.desc()).first().id  # 通过找到最后一个的id，用random.randint随机出每日推荐
    while True:
        random_today = Blog.query.filter_by(id=random.randint(1, last_id + 1)).first()
        if random_today is not None:
            break
    return random_today

@page.route('/')
def index():
    return render_template('index.html')

@page.route('/info')
@login_required
def info():
    return render_template('info.html')

@page.route('/blog')
def blog_index():
    topics = Topic.query.all()
    random_today = get_random_study()
    return render_template('blog_index.html', blog = random_today, topics =topics,)

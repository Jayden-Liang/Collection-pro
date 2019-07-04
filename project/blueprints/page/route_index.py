from flask import Blueprint, render_template, request
from flask_login import login_required
from project.blueprints.user.models import User, Role, Blog, Topic, Todo
import random

page = Blueprint('page', __name__, template_folder='templates')

# 全局变量
@page.context_processor
def my_context_processor():
    topics = Topic.query.all()
    return {'topics': topics,
            # 'admin' :
    }

# 辅助函数
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
    random_today = get_random_study()
    return render_template('blog_index.html', blog=random_today)

@page.route('/blog/new', methods=['POST','GET'])
def new():
    if request.method == 'POST':
        current_time = datetime.utcnow()
        username = current_user.username
        title = request.form.get('title')
        body = request.form.get('body')
        topic = request.form.get('topic')
        article = Blog(title= title,
                                body=body,
                                ct=current_time,
                                ut = current_time,
                                topic= topic,
                    )
        article.user_id = User.query.filter_by(username=username).first().id
        db.session.add(article)
        db.session.commit()
    return render_template('new_blog.html')

@page.route('/topic')
def blog_topic():
    topic = request.args.get('sort_by','')
    target = Topic.query.filter_by(body =topic).first()
    page = int(request.args.get('page'))
    if topic == 'All':
        articles = Blog.query.filter().order_by(Blog.ut.desc()).paginate(page, 8, False)
    else:
        #因为这里使用的关系型，Blog.topic == target,直接填入字符串是不行的
        articles = Blog.query.filter(Blog.topic == target).order_by(Blog.ut.desc()).paginate(page, 8, False)
    pages = articles.pages
    print(pages)
    return render_template('sort_by_topic.html', articles = articles,
                                                 topic= topic,
                                                 pages= pages
                                                     )

@page.route('/blog/detail')
def detail():
    blog_id = request.args.get('id','')
    article = Blog.query.get(blog_id)
    return render_template('blog_detail.html', article= article)

@page.route('/blog/delete')
def delete():
    pass

@page.route('/blog/update')
def update():
    pass

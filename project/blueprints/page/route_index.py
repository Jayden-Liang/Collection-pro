from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from project.blueprints.user.models import User, Role, Blog, Topic, Todo
from project.extensions import db
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup


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

#test for
@page.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@page.route('/ajax')
def testAjax():
    return render_template('test.html')

@page.route('/info')
@login_required
def info():
    return render_template('info.html')

@page.route('/blog')
def blog_index():
    random_today = get_random_study()
    return render_template('blog_index.html', blog=random_today)


@page.route('/blog/new', methods=['POST','GET'])
@login_required
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
                        ut = current_time
                    )
        user = User.query.filter_by(username=username).first()
        mytopic = Topic.query.filter_by(body = topic).first()
        mytopic.blogs.append(article)
        article.user_id = user.id
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('page.blog_topic', sort_by='All',page=1))
    return render_template('new_blog.html')

@page.route('/topic')
def blog_topic():
    q = None
    topic = request.args.get('sort_by','')
    page = request.args.get('p',1)
    #如果是搜索字符串
    # if data:
    #     articles = Blog.query.filter(Blog.title.like('%{}%'.format(data))).paginate(int(page), 8, False)
    #     topic = 'search'
    if topic == 'All':
        articles = Blog.query.filter().order_by(Blog.ut.desc()).paginate(int(page), 8, False)
    elif topic == 'search':
        q = request.args.get('query','')
        print(q)
        articles = Blog.query.filter(Blog.title.like('%{}%'.format(q))).paginate(int(page), 8, False)
    else:
        #因为这里使用的关系型，Blog.topic == target,直接填入字符串是不行
        target = Topic.query.filter_by(body =topic).first()
        articles = Blog.query.filter(Blog.topic == target).order_by(Blog.ut.desc()).paginate(int(page), 8, False)

    pages = articles.pages
    return render_template('sort_by_topic.html', articles = articles,
                                                 topic= topic,
                                                 pages= pages,
                                                 query = q)

@page.route('/blog/detail')
def detail():
    blog_id = request.args.get('id','')
    article = Blog.query.get(blog_id)
    return render_template('blog_detail.html', article= article)

@page.route('/blog/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        print(request.form)

        id = request.form.get('delete_id', None)
        if id:
            blog = Blog.query.get(int(id))
            if blog:
                db.session.delete(blog)
                db.session.commit()
                return redirect(url_for('page.blog_topic', sort_by='All',page=1))
            else:
                return '已经删除或不存在'
        else:
            return 'enheng'


@page.route('/blog/update', methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id = request.form.get('blog_id', None)
        title = request.form.get('title')
        body = request.form.get('body')
        topic = request.form.get('topic')
        if id and title and body and topic:
            blog = Blog.query.get(int(id))
            if blog:
                blog.ut = datetime.utcnow()
                blog.title = title
                blog.body = body
                mytopic = Topic.query.filter_by(body = topic).first()
                mytopic.blogs.append(blog)
                db.session.commit()
                return redirect(url_for('page.blog_topic', sort_by='All',page=1))
    id = request.args.get('article_id', None)
    if id:
        blog = Blog.query.get(int(id))
        if blog:
            return render_template('update.html', article = blog)


@page.route('/blog/news')
def news():
    r = requests.get('https://techcrunch.com/')
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all(class_='post-block__media')

    return  'hi'

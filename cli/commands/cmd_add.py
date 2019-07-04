import subprocess
from project.blueprints.user.models import User, Role, Blog, Topic, Todo
import click
from faker import Faker
import random
fake = Faker()
from project.app import create_app
from project.extensions import db
from flask import current_app

app = create_app()
db.app = app

@click.group()
def cli():
    """ add test users """
    pass


def add_role_account():
    admin = Role.query.filter_by(name='Admin').first()
    if admin is None:
        admin = Role(name= 'Admin')
        db.session.add(admin)
        db.session.commit()
    standard =Role.query.filter_by(name='Normal_Users').first()
    if standard is None:
        user = Role(name='Normal_Users')
        db.session.add(user)
        db.session.commit()

@click.command()
def roles():
    roles = ['Guest','Blocked','User','Moderator', 'Admin']
    for name in roles:
        db.session.add(Role(name=name))
        db.session.commit()
    print('添加role完毕')


@click.command()
def users():
    """
    generate users and data
    """
    user_emails = []
    data =[]
    for i in range(100):
        user_emails.append(fake.email())
    while True:
        email = user_emails.pop()
        user_set = {
              'username': fake.name(),
              'email': email,
              'password': User.encryptpassword('password'),
              'ct': fake.iso8601(tzinfo=None, end_datetime=None),
              'last_login_ip': fake.ipv4_private(),
              'current_login_ip': fake.ipv4_private()

        }
        data.append(user_set)
        if len(user_emails) <=0:
            break
    fisrt_admin = {
         'username': fake.name(),
         'email': app.config['SEED_ADMIN_EMAIL'],
         'password': User.encryptpassword(app.config['SEED_ADMIN_PASSWORD']),
         'ct': fake.iso8601(tzinfo=None, end_datetime=None),
         'last_login_ip': fake.ipv4_private(),
         'current_login_ip': fake.ipv4_private()
    }
    data.append(fisrt_admin)
    with app.app_context():
        db.drop_all()
        db.create_all()
        # User.query.delete()   #批量删除
        # db.session.commit()
        print('删除了')
        db.engine.execute(User.__table__.insert(), data)
        all = User.query.all()
        add_role_account()
        admin = Role.query.filter_by(name='Admin').first()
        user = Role.query.filter_by(name='Normal_Users').first()
        for u in all:
            i = random.random()
            if i <= 0.05:
                admin.users.append(u)
            else:
                user.users.append(u)
        db.session.commit()
        print('insert success')

@click.command()
def topics():
    import sqlite3
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Topic")
    result = cursor.fetchall()
    user = User.query.filter_by(email='liangjisong@foxmail.com').first()
    a =[]
    for r in result:
        a.append(r[1])
    a.remove('All')
    for x in a:
        # x =x.encode('utf8')
        topic = Topic(body=x)
        topic.user_id=user.id
        db.session.add(topic)
        db.session.commit()

@click.command()
def blogs():
    import sqlite3
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Blog")
    result = cursor.fetchall()
    user = User.query.filter_by(email='liangjisong@foxmail.com').first()
    for r in result:
        blog = Blog(title =r[1],
             body = r[2],
             ct = r[3],
             ut = r[6]
        )
        blog.user_id =user.id
        i=r[4]
        if i =='All':
            i = 'Flask'
        topic = Topic.query.filter_by(body=i).first()
        blog.topic_id = topic.id
        db.session.add(blog)
        db.session.commit()




@click.command()
def show():
    users = User.query.filter_by(email='liangjisong@foxmail.com').first()   #查看user的topics, blogs
    print(users.blogs)
    # for y in users.topics:
    #     print(y.body, y.id)
    # u = Topic.query.all()
    # for x in u:
    #     print(x.body)
    # topic = Topic.query.filter_by(body='Python').first()     #查看topic的blogs
    # print(topic.blogs)





cli.add_command(users)
cli.add_command(topics)
cli.add_command(blogs)
cli.add_command(show)

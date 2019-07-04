from flask_login import UserMixin
from project.extensions import db
from sqlalchemy import or_

import bcrypt



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index= True,unique=True)
    email = db.Column(db.String(64), unique = True, index=True)
    password = db.Column(db.String(128), nullable=False, server_default='')
    ct = db.Column(db.DateTime())
    active = db.Column(db.Integer)

    latest_online = db.Column(db.DateTime())


    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates= 'users')
    # active = db.Column('is_active', db.Boolean(), nullable=False,
    #                    server_default='1')

    blogs = db.relationship('Blog', back_populates='user')

    topics = db.relationship('Topic', back_populates='user')

    todos = db.relationship('Todo', back_populates='user')

    recipes = db.relationship('Recipe', back_populates='user')

    sign_in_count = db.Column(db.Integer, nullable=False, default=0)    #如果ip不一样，那么这里加1
    last_login_time = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(128))

    current_login_time = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(128))

    @classmethod
    def encryptpassword(cls, password, salt='$!@>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2


    def passwordmatch(self, password=''):
        return self.password == User.encryptpassword(password)

    @classmethod
    def find_by_identity(cls, identity):
        return User.query.filter(or_(User.username == identity, User.email == identity)).first()


    def save(self):
        db.session.add(self)
        db.session.commit()
        return None

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index= True)
    users = db.relationship('User', back_populates= 'role')

class Blog(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(10000))
    ct = db.Column(db.DateTime())
    ut = db.Column(db.DateTime())

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship('Topic', back_populates='blogs')


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='blogs')


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(100))
    blogs = db.relationship('Blog', back_populates='topic')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='topics')





class Todo(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(120))
    done = db.Column(db.Integer)
    ct =db.Column(db.DateTime())
    finished_time = db.Column(db.DateTime())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='todos')

    def __repr__(self):
        return '<Todo {}>'.format(self.body)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ingredients = db.Column(db.String(500))
    steps = db.Column(db.String(1500))
    ct =db.Column(db.DateTime())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='recipes')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='recipes')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(120))

    recipes = db.relationship('Recipe', back_populates='category')

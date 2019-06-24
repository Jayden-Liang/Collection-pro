from project.extensions import db


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(64), index= True,unique=True)
#     email = db.Column(db.String(64), unique = True)
#     hashed_password = db.Column(db.String(128))
#     ct = db.Column(db.DateTime())
#
#
#     @classmethod
#     def salted_password(cls, password, salt='ad^&6x678$6$4h3245&DWQa'):
#         import hashlib
#         def sha256(ascii_str):
#             return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
#         hash1 = sha256(password)
#         hash2 = sha256(hash1 + salt)
#         return hash2


class Blog(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    body = db.Column(db.String())
    ct = db.Column(db.DateTime())
    ut = db.Column(db.DateTime())

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship('Topic', back_populates='blogs')

    from project.blueprints.user.models import User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='blogs')


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(128))
    blogs = db.relationship('Blog', back_populates='topic')



class Todo(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String())
    done = db.Column(db.Integer)
    ct =db.Column(db.DateTime())
    finished_time = db.Column(db.DateTime())

    def __repr__(self):
        return '<Todo {}>'.format(self.body)


from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from project.blueprints.user.models import User, Role, Blog, Topic, Todo
from flask_login import login_required, current_user
from project.extensions import db


todo = Blueprint('todo', __name__, template_folder='templates')
from datetime import datetime


# 全局变量

@todo.context_processor
def my_context_processor():
    if current_user.is_anonymous:
        topics = User.query.filter_by(email='liangjisong@foxmail.com').first().topics
    else:
        topics = current_user.topics
    return {'topics': topics,
            # 'admin' :
    }


@todo.route('/todo')
@login_required
def index():
    todos = User.query.filter_by(username=current_user.username).first().todos
    return render_template('todo.html', todos = todos)

@todo.route('/todo/finished')
@login_required
def finished():
    todos = User.query.filter_by(username=current_user.username).first().todos
    return render_template('finished.html', todos = todos)

@todo.route('/todo/add', methods=['post'])
@login_required
def add():
    data = request.get_json()
    todo = data.get('todo')
    if len(todo)<= 50:
        t = Todo(body=todo,
                 done = 0,
                 ct = datetime.utcnow(),
          )
        user = User.query.filter_by(username=current_user.username).first()
        t.user_id = user.id
        db.session.add(t)
        db.session.commit()
        return jsonify({'id': t.id})
    else:
        return jsonify('字数超过')




@todo.route('/todo/delete', methods=['post'])
@login_required
def delete():
    data  = request.get_json()
    id = data.get('todo')
    todo = Todo.query.get(int(id))
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return jsonify('deleted data')

@todo.route('/todo/finish', methods=['post'])
@login_required
def finish():
    data  = request.get_json()
    id = data.get('todo')
    todo = Todo.query.get(int(id))
    if todo:
        todo.done = 1
        db.session.commit()
        return jsonify('done')

from flask import Flask
from celery import Celery
from project.blueprints.page.route_index import page
from project.blueprints.user.views import user
from project.blueprints.admin.views import admin
from project.blueprints.user.models import User
from project.extensions import  csrf, db, login_manager, moment
from datetime import datetime

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
    if settings_override is not None:
        app.config.update(settings_override)
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    extension(app)
    authentication(app)
    return app

#celery
CELERY_TASK_LIST =[
    'project.blueprints.user.celery_task'
]
#celery
def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):                #以下是为每个task设置context，如果要access数据库，就要设置context
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def extension(app):
    print('hi there')
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    return None

def authentication(app):
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(uid):
        u = User.query.get(uid)
        # if u is not None:
        #     u.latest_online = datetime.utcnow
        #     u.save()
        return u

from flask import Flask, render_template
from celery import Celery
from werkzeug.contrib.fixers import ProxyFix
from project.blueprints.page.route_index import page
from project.blueprints.user.views import user
from project.blueprints.todo.views import todo
from project.blueprints.contact.views import contact
from project.blueprints.admin.views import admin
from project.blueprints.recipe.views import recipe
from project.blueprints.user.models import User
from project.blueprints.others.views import Burger
from project.blueprints.api.views import api
from project.extensions import  csrf, db, login_manager, moment, dropzone, mail
from datetime import datetime

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)
    app.config['JSON_AS_ASCII']=False
    # app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
    if settings_override is not None:
        app.config.update(settings_override)
    # print(app.config['TEST_STRING'])
    app.logger.setLevel(app.config['LOG_LEVEL'])
    middleware(app)
    register_errorhandlers(app)
    blueprints(app)
    extension(app)
    authentication(app)
    return app


#blueprints
def blueprints(app):
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(recipe)
    app.register_blueprint(todo)
    app.register_blueprint(contact)
    app.register_blueprint(Burger)
    app.register_blueprint(api)


#ProxyFix
def middleware(app):
        app.wsgi_app = ProxyFix(app.wsgi_app)
        return None

#celery


CELERY_TASK_LIST =[
    'project.blueprints.user.celery_task',
    'project.blueprints.contact.celery_task',
    'project.celery.celery_task'
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
    dropzone.init_app(app)
    mail.init_app(app)
    return None

def authentication(app):
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(uid):
        u = User.query.get(uid)
        if u is not None:
            ct = datetime.utcnow()
            u.latest_online = ct
            #转换datetime.fromtimestamp(timestamp)
            u.save()
        return u

def register_errorhandlers(app):
        def render_error(error):
            error_code = getattr(error, 'code', 500)                        #获得error对象的code属性值，默认为500
            return render_template("errors/{0}.html".format(error_code)), error_code

        for errcode in [404, 500]:
            app.errorhandler(errcode)(render_error)
        return None

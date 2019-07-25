import os
from dotenv import load_dotenv
b = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(b, '.env')
load_dotenv(dotenv_path=env_path)

# DEBUG = True
LOG_LEVEL = 'DEBUG'   #CRITICAL / ERROR / WARNING / INFO / DEBUG    DEBUG已经包含来其他几种类型
# SERVER_NAME = 'hit-the-road.cc'
SECRET_KEY = 'dev secret key'  #os.getenv('SECRET_KEY')

#flask dropzone
# MAX_CONTENT_LENGTH =3*1024*1024
DROPZONE_ENABLE_CSRF = True
DROPZONE_MAX_FILE_SIZE =3
DROPZONE_MAX_FILES= 30
DROPZONE_SAVE_PATH='static/pics'


# SQLAlchemy.
db_uri = 'mysql+mysqldb://jayden:devpassword@mysql:3306/collection?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

SEED_ADMIN_EMAIL = 'liangjisong@foxmail.com'
SEED_ADMIN_PASSWORD = '123456'

#flask-Mail
# QQ邮箱
# MAIL_SERVER='smtp.qq.com'
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME =os.getenv('MAIL_USERNAME')
# MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
# MAIL_DEFAULT_SENDER = (os.getenv('MAIL_USERNAME'))
#
# MAIL_PASSWORD='xjnyvzlafzrbbceg'
# 163邮箱
MAIL_SERVER='smtp.163.com'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME =os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = (os.getenv('MAIL_USERNAME'))
# sendgrid
SENDGRID_API_KEY=os.getenv('SENDGRID_KEY')
#Celery
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'          #0代表默认的redis数据库名称
CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']                    #这几行表示只接受json格式和序列化成json
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 30    # 防止redis因连接过多挂掉， 这里是开发环境限制5个

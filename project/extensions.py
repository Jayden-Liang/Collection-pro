from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_dropzone import Dropzone



csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
moment =Moment()
dropzone = Dropzone()

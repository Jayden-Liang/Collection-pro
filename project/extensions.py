from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment



csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
moment =Moment()

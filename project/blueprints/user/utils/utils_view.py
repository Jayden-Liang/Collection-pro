from flask import redirect, render_template, current_app
from functools import wraps
from project.blueprints.user.models import User
from flask_login import current_user
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, \
    TimedJSONWebSignatureSerializer

from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import Email, Content, Mail


def anonymity_required(url='/settings'):
    def decorator(f):
        @wraps(f)
        def decorator_func(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url)
            return f(*args, **kwargs)
        return decorator_func
    return decorator

def track_activity(u, ip):
    current_time = datetime.utcnow()
    u.last_login_time = u.current_login_time
    u.last_login_ip = u.current_login_ip

    u.current_login_time = current_time
    u.current_login_ip = ip
    u.save()


def serializer(email):
    serializer = TimedJSONWebSignatureSerializer(current_app.config.get('SECRET_KEY'), 3600)
    s = serializer.dumps({'user_email': email}).decode('utf-8')
    return s

def deserializer(token):
    serializer = TimedJSONWebSignatureSerializer(current_app.config.get('SECRET_KEY'))
    user_email = serializer.loads(token).get('user_email')
    return User.find_by_identity(user_email)




# def sendgrid_email(email, to, **kwargs):
#     message = {
#     'personalizations': [
#         {
#             'to': [
#                 {
#                     'email': to
#                 }
#             ],
#             'subject': 'Resetting Password'
#         }
#     ],
#     'from': {
#         'email': email
#     },
#     'content': [
#         {
#             'type': 'text/plain',
#             'value': render_template('email/sendgrid_template.txt', **kwargs)
#         }
#      ]
#     }
#     from config import settings
#     sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
#     response = sg.send(message)

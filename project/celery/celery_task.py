
from flask import redirect, render_template, current_app
from sendgrid import SendGridAPIClient
from project.app import create_celery_app
celery = create_celery_app()
import requests

from flask_mail import Message
from project.extensions import mail


def send_without_celery(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)
    return None


@celery.task()
def send_mail(subject, to, body):
    print('i use another one')
    send_without_celery(subject, to, body)



@celery.task()
def sendgrid_email(email, to, **kwargs):
    message = {
    'personalizations': [
        {
            'to': [
                {
                    'email': to
                }
            ],
            'subject': 'Resetting Password'
        }
    ],
    'from': {
        'email': email
    },
    'content': [
        {
            'type': 'text/plain',
            'value': render_template('email/sendgrid_template.txt', **kwargs)
        }
     ]
    }
    from config import settings
    print(settings.SENDGRID_API_KEY)
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    print(response)
    return None

@celery.task()
def mailgun_email(email, to, **kwargs):  #需要绑定信用卡，
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc335ce4005234d40b18ea4389be35025.mailgun.org",
        auth=("api", "5be29df2ead15d7b9b08fb53fc8674af-c50f4a19-9a2774a5"),
        data={"from": "Mailgun Sandbox <mailgun@sandboxc335ce4005234d40b18ea4389be35025.mailgun.org",
              "to": "807570635@qq.com",
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

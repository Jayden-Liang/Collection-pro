from flask import redirect, render_template, current_app
from project.app import create_celery_app
celery = create_celery_app()
from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import Email, Content, Mail

# @celery.task()
# def deliver_email(email, message):
#     ctx ={'email':email, 'message': message}
#     send_template_message(
#                          subject='my kindest greetings',
#                          sender=email,
#                          recipients=[celery.conf.get('MAIL_USERNAME')],
#                          reply_to=email,
#                          template='contact/mail/index',ctx=ctx
#     )
#
#     return None

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
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    print(response)
    return None

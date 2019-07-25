
from flask import redirect, render_template, current_app

from project.app import create_celery_app
celery = create_celery_app()


@celery.task()
def send_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)
    return None

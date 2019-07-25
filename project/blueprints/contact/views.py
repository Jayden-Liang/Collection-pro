from flask import redirect, render_template, Blueprint, request, flash, current_app, url_for, flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email





contact = Blueprint('contact', __name__, template_folder='templates' )



class ContactForm(FlaskForm):
    name = StringField('Hello, what is your name?', [DataRequired(message='不能为空'), Length(3, 10, message='3-10个字符')])
    email = StringField('What is your email?', [DataRequired(message='不能为空'), Length(3,50, message='太长或太短'), Email(message='不是邮箱')])
    content = TextAreaField('Words you want to say', [DataRequired(message='不能为空'), Length(3, 500, message='需在500字以内' )] )



@contact.route('/contact', methods=['POST', 'GET'])
def contact_index():
    from project.celery.celery_task  import send_mail
    from project.celery.celery_task  import send_without_celery
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        send_without_celery('你好，{}'.format(name), email, u'我已收到你的邮件，稍后回复你')
        # send_without_celery('Guest', '807570635@qq.com', '{} said: {}, from email {}'.format(name,form.content.data, email))
        flash(u'邮件发送成功')
        print('flashed')
        # send_mail.delay('你好，{}'.format(name), email, u'我已收到你的邮件，稍后回复你')
        # send_mail.delay('Guest', '807570635@qq.com', '{} said: {}, from email {}'.format(name,form.content.data, email))
        return redirect(url_for('contact.contact_index'))
    return render_template('contact.html', form = form)

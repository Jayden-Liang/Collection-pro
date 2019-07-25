from flask import redirect, render_template, Blueprint, request, flash, url_for, flash
from project.blueprints.user.forms import sayhi, LoginForm, signupForm, getuserForm, update_emailForm, update_pwdForm, find_pwdForm, set_newpwdForm
from project.blueprints.user.models import User
from datetime import datetime
from flask_login import login_required, login_user, current_user, logout_user
from project.blueprints.user.utils.utils_view import anonymity_required, track_activity, serializer, deserializer
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

user = Blueprint('user', __name__, template_folder='templates' )

#登入
@user.route('/login', methods=['POST', 'GET'])
@anonymity_required()
def login():
    form = LoginForm(next=request.args.get('next'))
    if form.validate_on_submit():
        next = request.form.get('next')
        identity = form.identity.data
        password = form.password.data
        u = User.find_by_identity(identity)
        if u and u.passwordmatch:
            login_user(u, remember=False)
            # print('看看environ', request.environ)
            track_activity(u, request.environ.get('HTTP-X_REAL_IP', request.remote_addr))
            if next:
                return redirect(urljoin(request.host_url, next))
            else:
                return redirect(url_for('user.settings'))
        else: flash('密码或帐号不正确')

    return render_template('login.html', form=form)

#登出
@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('page.index'))

#注册
@user.route('/signup', methods=['POST', 'GET'])
@anonymity_required()
def signup():
    form = signupForm()
    if form.validate_on_submit():
        print('received')
        u = User(
                email= form.email.data,
                password = User.encryptpassword(form.password.data))
        u.ct = datetime.utcnow()
        u.save()
        if login_user(u):
            track_activity(u, request.remote_addr)
            return redirect(url_for('user.welcome'))
    return render_template('signup.html', form = form)


#注册成功后的欢迎页面，在这个页面提示用户取用户名
@user.route('/welcome', methods=['POST', 'GET'])
@login_required
def welcome():
    if current_user.username:
        print('you already have a username')
        return redirect(url_for('user.settings'))
    form = getuserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.save()
        return redirect(url_for('user.settings'))
    return render_template('welcome.html', form =form)

@user.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    return render_template('settings.html')

#更改邮箱页面
@user.route('/settings/update_email', methods=['POST', 'GET'])
@login_required
def update_email():
    form = update_emailForm()
    if form.validate_on_submit():
        print('received data')
        u = User.find_by_identity(form.email.data)
        if u and u.passwordmatch(password=form.curent_password.data):
            print('passed validation')
            u.email = form.new_email.data
            u.save()
            return redirect(url_for('user.settings'))
        else:
            return '密码不对'
    return render_template('update_email.html', form=form)

#更改密码页面
@user.route('/settings/update_pwd', methods=['POST', 'GET'])
@login_required
def update_pwd():
    form = update_pwdForm()
    if form.validate_on_submit():
        u = User.find_by_identity(form.identity.data)
        if u and u.passwordmatch(password=form.curent_password.data):
            u.password = User.encryptpassword(form.curent_password.data)
            u.save()
            return redirect(url_for('user.settings'))
        else:
            return '密码或邮箱不正确'

    return render_template('update_pwd.html', form=form)


#忘记密码重置页面
@user.route('/find_pwd', methods=['POST', 'GET'])
def find_pwd():
    form = find_pwdForm()
    if form.validate_on_submit():
        token = serializer(form.email.data)
        from project.celery.celery_task import send_mail, send_without_celery
        send_without_celery('密码重置', form.email.data, '请点击链接{}'.format(url_for('user.set_new_pwd', reset_token = token, _external =True)))
        return redirect('/')
    return render_template('find_pwd.html', form = form)

#忘记密码重置页面 - 更改页面
@user.route('/settings/set-new-pwd', methods=['POST', 'GET'])
def set_new_pwd():
    form = set_newpwdForm(reset_token=request.args.get('reset_token'))
    if form.validate_on_submit():
        print('reset_token',request.form.get('reset_token'))
        token = request.form.get('reset_token')
        u= deserializer(token)
        if u:
            u.password = u.encryptpassword(form.new_pwd.data)
            u.save()
            login_user(u)
            track_activity(u, request.remote_addr)
            print('password has been reset')
            return redirect( url_for('user.settings'))
        else:
            return 'the token is expired or tamperd with'


    return render_template('set_new_pwd.html', form= form)

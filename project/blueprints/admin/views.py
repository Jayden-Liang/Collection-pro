from flask import redirect, render_template, Blueprint, request, flash, url_for
from project.blueprints.user.forms import sayhi, LoginForm, signupForm, getuserForm, update_emailForm, update_pwdForm, find_pwdForm, set_newpwdForm
from project.blueprints.user.models import User, Role
from flask_login import login_required, login_user, current_user, logout_user
from project.blueprints.admin.utils.utils_views import test_decor
from project.blueprints.admin.forms import SearchBox
from project.blueprints.user.models import User
from sqlalchemy import or_

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix = '/admin' )

@admin.before_request
@test_decor()
@login_required
def before_request():
    print('this is before_request')

@admin.route('', methods=['GET', 'POST'])
def index():
    form = SearchBox()
    page = int(request.args.get('page',1))
    starter = int(request.args.get('starter', 1))
    identity =request.args.get('identity')
    if identity is not None:
        users = User.query.filter(or_(User.username.like('%{}%'.format(identity)),User.email.like('%{}%'.format(identity)))).order_by(User.id.desc()).paginate(page, 10, False)
    else:
        users = User.query.filter().order_by(User.id.desc()).paginate(page, 10, False)
    pages = users.pages
    print('how many pages?',pages)
    if request.method== 'POST':
        print(request.form)
    return render_template('admin_index.html',
                            users = users,
                            pages = pages,
                            current_page = page,
                            starter = starter,
                            identity = identity,
                            form = form)


@admin.route('/user')
def user():
    return 'user page'

@admin.route('/search', methods=['POST'])
def search():
    form = SearchBox()
    if form.validate_on_submit():
        print('received search data')
        data = request.form                       #找到目标并显示
        identity = data.get('identity','')
        # if identity=='' or identity is None:
        # users = User.query.filter().order_by(User.id.desc()).paginate(1, 10, False)

        users = User.query.filter(User.username.like('%{}%'.format(identity))).order_by(User.id.desc()).paginate(1, 10, False)


        pages = users.pages
        return render_template(
                           'admin_index.html',
                           users = users,
                           pages = pages,
                           current_page = 1,
                           starter = 1,
                           form =form
        )

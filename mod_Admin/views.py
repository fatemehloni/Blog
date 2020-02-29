from . import admin
from flask import session, render_template, request, abort
from mod_Users.forms import LoginForm
from mod_Users.models import User


@admin.route('/')
def index():
    return "hello from admin index"


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        user = User.query.filter(User.email.ilike(f"{form.email.data}")).first()
        if not user:
            return "incorrect user"
        if not user.check_password(form.password.data):
            return "incorrect password"
        session['email'] = user.email
        session['user_id'] = user.id
        return "Login success"
    if session.get('email') is not None:
        return "You are already logged in."

        print(user)
    return render_template('admin/login.html', form=form)

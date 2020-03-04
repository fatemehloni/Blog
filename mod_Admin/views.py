from . import admin
from flask import session, render_template, request, abort, flash
from mod_Users.forms import LoginForm
from mod_Users.models import User
from .Utils import admin_only_view


@admin.route('/')
@admin_only_view
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
            flash('incorrect user', category='error')
            return render_template('admin/login.html', form=form)
        if not user.check_password(form.password.data):
            flash('incorrect password', category='error')
            return render_template('admin/login.html', form=form)
        if not user.is_admin():
            flash('You do not have admin access ', category='error')
            return render_template('admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role
        return "Login success"
    if session.get('role') == 1:
        return "You are already logged in."

        print(user)
    return render_template('admin/login.html', form=form)

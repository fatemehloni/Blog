from flask import request, render_template, flash
from . import users
from .forms import RegisterForm
from .models import User
from sqlalchemy.exc import IntegrityError
from app import db


@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('users/register.html', form=form)
        if not form.password.data == form.confirm_password.data:
            error_msg = 'password and confirm password does not mach'
            form.password.errors.append(error_msg)
            form.confirm_password.errors.append(error_msg)
            return render_template('users/register.html', form=form)
        new_user = User()
        new_user.fullname = form.full_name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('You created your account successfully.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('email is in use.', 'error')

    return render_template('users/register.html', form=form)

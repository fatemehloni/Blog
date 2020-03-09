from . import admin
from flask import session, render_template, request, abort, flash, redirect, url_for
from mod_Users.forms import LoginForm, RegisterForm
from mod_Users.models import User
from .Utils import admin_only_view
from mod_blog.form import CreatePostForm, ModifyPostForm, CategoryForm
from mod_blog.models import Post, Category
from app import db
from sqlalchemy.exc import IntegrityError


@admin.route('/')
@admin_only_view
def index():
    return render_template('admin/index.html')


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
        return redirect(url_for('admin.index'))
    if session.get('role') == 1:
        return redirect(url_for('admin.index'))

    return render_template('admin/login.html', form=form)


@admin.route('/users/', methods=['GET'])
@admin_only_view
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/list_users.html', users=users)


@admin.route('/users/new', methods=['GET', 'POST'])
@admin_only_view
def create_user():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/create_user.html', form=form)
        if not form.password.data == form.confirm_password.data:
            error_msg = 'password and confirm password does not mach'
            form.password.errors.append(error_msg)
            form.confirm_password.errors.append(error_msg)
            return render_template('admin/create_user.html', form=form)
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

    return render_template('admin/create_user.html', form=form)


@admin.route('/posts/')
@admin_only_view
def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/list_posts.html', posts=posts)


@admin.route('/posts/delete/<int:post_id>/', methods=['GET', 'POST'])
@admin_only_view
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.')
    return redirect(url_for('admin.list_posts'))


@admin.route('/posts/modify/<int:post_id>/', methods=['GET', 'POST'])
@admin_only_view
def modify_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = ModifyPostForm(obj=post)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_post.html', form=form, post=post)
        post.title = form.title.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.content = form.content.data
        try:
            db.session.commit()
            flash('Post modified.')
        except IntegrityError:
            db.session.rollback()
            flash('Duplicated slug.')
    return render_template('admin/modify_post.html', form=form, post=post)


@admin.route('/logout/', methods=['GET'])
@admin_only_view
def logout():
    session.clear()
    flash('you logged out ', 'warning')
    return redirect(url_for('admin.login'))


@admin.route('/posts/new', methods=['GET', 'POST'])
@admin_only_view
def create_post():
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/create_post.html')
        new_post = Post()
        new_post.title = form.title.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data
        new_post.summary = form.summary.data
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post Created!')
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Duplicated slug.')

    return render_template('admin/create_post.html', form=form)


@admin.route('/categories/new', methods=['GET', 'POST'])
@admin_only_view
def create_category():
    form = CategoryForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/create_post.html')
        new_category = Category()
        new_category.name = form.name.data
        new_category.slug = form.slug.data
        new_category.description = form.description.data

        try:
            db.session.add(new_category)
            db.session.commit()
            flash('Category Created!')
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Duplicated slug.')

    return render_template('admin/create_category.html', form=form)


@admin.route('/categories/')
@admin_only_view
def list_categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/list_categories.html', categories=categories)


@admin.route('/categories/delete/<int:category_id>/', methods=['GET', 'POST'])
@admin_only_view
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted.')
    return redirect(url_for('admin.list_categories'))


@admin.route('/posts/modify/<int:category_id>/', methods=['GET', 'POST'])
@admin_only_view
def modify_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_category.html', form=form, category=category)
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        try:
            db.session.commit()
            flash('Category modified.')
        except IntegrityError:
            db.session.rollback()
            flash('Duplicated slug.')
    return render_template('admin/modify_category.html', form=form, category=category)

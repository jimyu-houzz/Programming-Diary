from flask import render_template, url_for, flash, redirect, request, Blueprint
from blog import db, bcrypt
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            RequestResetForm, ResetPasswordForm)
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
# import custom functions
from blog.users.utils import save_picture, send_reset_email

# exporting the USERS package
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # So the user doesn't go to register page when signed in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # create user instance and add to db
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # flash message can be parsed into html for frontend layout
        flash(f'Your account: {form.username.data} has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # get user
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) # remember is a boolean input
            # don't use args['next'] or will show error when key doesn't exist
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unseccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# see or update account info
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    # if the user wants to update account info
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # don't use render_template here, so the browser doesn't submit the form twice
        return redirect(url_for('users.account'))
    # if user just navigates to account page
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                            image_file=image_file, form=form)
            

# get all posts from a specific user
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


# reset password STEP 1
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # we want user to be logged out, if logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# reset password STEP 2
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # static method from User model, returns User or None
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        # redirect to the page to generate token
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now albe to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
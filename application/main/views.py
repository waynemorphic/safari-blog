from urllib import request
from flask import Flask, render_template, url_for, redirect, flash, abort
from ..models import User, Post, Comment
from application.auth.forms import RegistrationForm, LoginForm, PostForm, CommentForm, UpdateProfile
from . import main
from application import db, photos
from flask_login import login_required, login_user, logout_user, current_user


# index route
@main.route('/')
def index():
    '''
    function to define index template
    '''
    
    title = 'PostAPitch'
    
    return render_template('index.html', title = title)

# @main.route('/posts')
# def posts():
#     '''
#     function defines all the posts in the application
#     '''
#     title = 'PostAPitch'
#     return render_template()

# log in
@main.route('/login', methods=['GET', 'POST'])
def login():
    '''
    function to define user login case
    '''
    
    title = 'PostAPitch'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(url_for('main.index'))
        flash('Invalid Username or Password', 'danger')
        
    return render_template('auth/login.html', title = title, form = form)

# registration
@main.route('/register', methods=['GET', 'POST'])
def registration():
    '''
    function to define registration case
    '''
    
    title = 'PostAPitch'
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful', 'message')
        return redirect(url_for('main.index'))
    
    return render_template('auth/registration.html', title = title, form = form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


# user profile
@main.route('/user/<uname>')
def profile(uname):
    '''
    function to define user profile
    '''
    
    title = current_user.username
    user = User.query.filter_by(username = uname).first()
    
    if user is None:
        abort (404)
    return render_template('user/profile.html', title = title, user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
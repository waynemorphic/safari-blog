from flask import Flask, render_template, url_for, redirect
from . import main
from flask_login import login_required, login_user, logout_user, current_user

# index route
@main.route('/')
def index():
    '''
    function to define index template
    '''
    
    title = 'PostAPitch'
    
    return render_template('index.html', title = title)

# log in
@main.route('/login')
def login():
    '''
    function to define user login case
    '''
    
    title = 'PostAPitch'
    
    return render_template('auth/login.html', title = title)

# registration
@main.route('/register')
def registration():
    '''
    function to define registration case
    '''
    
    title = 'PostAPitch'
    
    return render_template('auth/registration.html', title = title)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.login"))

# user profile
@main.route('/')
def profile():
    '''
    function to define user profile
    '''
    
    title = 'PostAPitch'
    
    return render_template('user/profile.html', title = title)

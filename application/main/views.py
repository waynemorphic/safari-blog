from urllib import request
from flask import Flask, render_template, url_for, redirect, flash, abort
from ..models import User, Post, Comment
from application.auth.forms import RegistrationForm, LoginForm, PostForm, CommentForm, UpdateProfile
from . import main
from application import db, photos
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from ..requests import generate_quote, random_quotes


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# index route
@main.route('/')
def index():
    '''
    function to define index template
    '''
    
    title = 'SAFARIYANYIKA'
    quote = random_quotes()
    quotes = generate_quote(1, random_quotes)
    return render_template('index.html', title = title, quotes = quotes)

# adding a blog
@main.route('/addblog', methods=['GET', 'POST'])
@login_required
def add_blog():
    '''
    function adds user blogs in the application
    '''
    title = 'SAFARIYANYIKA'
    user = User.query.first()
    form = PostForm()
   
    if form.validate_on_submit():
        add_post = Post(post_stuff = form.post_stuff.data )
        add_post.save_post()
        
        flash("Blog posted!", "success")
        
        return redirect(url_for('main.blogs'))
    return render_template('add_blog.html', title = title, form = form)

# blogs in the website
@main.route('/blogs', methods=['GET', 'POST'])
def blogs():
    '''
    function renders the blogs template
    '''
    title = 'SAFARIYANYIKA'
    blogs = Post.query.all()
    users = User.query.all()
    
    return render_template('blogs.html', title = title, blogs = blogs, users = users)

# blog comments
@main.route('/blogs/comment/new/int:<post_id>', methods = ['GET', 'POST'])
@login_required
def add_comment(post_id):
    '''
    adds comment to a blog
    '''
    
    blog_comment = Post.query.filter_by(id = post_id).first().post_stuff
    print(blog_comment)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        added_comment = Comment(comment_stuff = comment_form.comment_stuff.data, user = current_user, post_id = post_id)
        added_comment.save_comment()
        flash('Comment added successfully', 'success')
        return redirect(url_for('main.blogs', post_id = post_id))
    
    all_comments = Comment.get_comment(post_id)
    print(all_comments)

    return render_template('comment.html', comment_form = comment_form, blog_comment = blog_comment, all_comments = all_comments)

# delete a blog
@main.route('/blogs', methods = ['POST'])
@login_required
def delete_comment(post_id, comment_id):
    post= Post.get_post(post_id)
    comment = Comment.get_comment(comment_id)
    
    if post.user != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', 'success')
    return render_template('main.blogs', post_id = post.id) 
    
# log in
@main.route('/login', methods=['GET', 'POST'])
def login():
    '''
    function to define user login case
    '''
    
    title = 'SAFARIYANYIKA'
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
    
    title = 'SAFARIYANYIKA'
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful', 'message')
        return redirect(url_for('main.login'))
    
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


@main.route('/user/<uname>/update/pic',methods= ['GET', 'POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # If the user does not select a file, the browser submits an
    #     # empty file without a filename.
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))   
    
    # files = {'file': open('static')}
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
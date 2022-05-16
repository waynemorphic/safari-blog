from application import db
from datetime import datetime
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    '''
    user class
    Args:
    username, email, bio, image_file, pass_hash, posts
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    image_file = db.Column(db.String(20), default = 'default.jpeg')
    pass_hash = db.Column(db.String(255))
    posts = db.relationship('Post', backref = 'author', lazy = True) 
    comment_stuff = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    

    # save the user
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    
    # write only class property
    @property 
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password)    :
        self.pass_hash = generate_password_hash(password)
        
        
    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)
    
    # querying database for specific user
    @login_manager.user_loader 
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    def __repr__(self):
        return f"User ({self.username }, { self.email}, {self.image_file})"
    
class Post(db.Model):
    '''
    class defines the posts
    Args:
        title, content, date_posted, upvote, downvote, category
    '''
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    post_stuff = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    comment_stuff = db.relationship('Comment', backref = 'post', lazy = 'dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # referencing the table name users and the column name id
    
    # saving the post
    def save_post(self):
        db.session.add(self)
        db.session.commit()
    
    # getting post id
    @classmethod
    def get_post_id(cls, id):
        post_id = Post.query.filter_by(id = id).order_by(Post.id.desc())
        return post_id
    
    @classmethod
    def get_user_post(cls):
        user_post = Post.query.all()
        return user_post
    
    def __repr__(self):
        return f'Post {self.date_posted}, {self.post_stuff}'
    
class Comment(db.Model):
    '''
    class defines the user comments
    '''
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    comment_stuff = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    # saving the comment
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    
    # get comment by post
    @classmethod
    def get_comment(cls, id):
        the_comment = Comment.query.filter_by(post_id = id).all()
        return the_comment
    
    def __repr__(self):
        return f"Comment {self.comment_stuff}"

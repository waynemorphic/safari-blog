from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    '''
    class for identifying login fields
    '''
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    '''
    class for identifying registration form
    '''
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=20)])
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Sign up')
    
    # validating new users registering in the platform
    def validate_email(self,data_field):
        if User.query.filter_by(email =data_field.data).first():
            raise ValidationError('Account with that email exists')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('Username is taken')
    
class CommentForm(FlaskForm):
    '''
    class for taking user comments on posts
    '''
    comment_stuff = TextAreaField('Leave a Comment')
    submit = SubmitField('Post')

class PostForm(FlaskForm):
    '''
    class defines user pitches posted on the platform
    '''
    title_stuff = StringField('Blog Title')
    post_stuff = TextAreaField('Blog Content', validators=[InputRequired(), Length(min=20)])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')
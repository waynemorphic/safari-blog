from flask import Flask, render_template
from . import main
# from application import app

# index route
@main.route('/')
def index():
    '''
    function to define index template
    '''
    
    title = 'PostAPitch'
    
    return render_template('index.html', title = title)

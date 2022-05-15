from venv import create
from application import create_app, db
from flask_script import Manager,Server
from application.models import User, Post, Comment

app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User, Post = Post, Comment = Comment )


if __name__ == '__main__':
    manager.run()
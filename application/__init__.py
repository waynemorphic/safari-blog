from flask import Flask
from .config import DevConfig
from flask_bootstrap import Bootstrap
from .config import config_options

bootstrap = Bootstrap()

# app = Flask(__name__)

# app.config.from_object(DevConfig)

# from .main import views

def create_app(config_name):
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    bootstrap.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# from .config import DevConfig
# from flask_bootstrap import Bootstrap
# from .config import config_options
# from . import views


# bootstrap = Bootstrap()


# def create_app(config_name):
#     app = Flask(__name__)
    
#     app.config.from_object(config_options[config_name])
    
#     bootstrap.init_app(app)
    
    
#     return app
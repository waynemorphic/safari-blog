import os

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = '987654321'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wayne:123@localhost/safaridb'
    UPLOADED_PHOTOS_DEST ='app/static/photos'

class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    
    DEBUG = True
    
config_options = {
'development':DevConfig,
'production':ProdConfig
}
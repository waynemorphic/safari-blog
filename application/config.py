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
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    
    DEBUG = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wayne:123@localhost/safaridb'
    
config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}
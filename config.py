import os 
# configure env variable

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_clé_secrète_très_sécurisée'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///blogging_platform.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
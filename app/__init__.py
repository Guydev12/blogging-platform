from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import Config 
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialisation of SQLAlchemy
db = SQLAlchemy()
# Initialize the login manager without app
login_manager = LoginManager()
def create_app():
  # Initialize the app
  app = Flask(__name__)
  app.config.from_object(Config)
  migrate = Migrate(app,db)
  # Initialize the db within the app
  db.init_app(app)
  # Link login_manager with app
  login_manager.init_app(app)
  # Handle unauthebticated user
  login_manager.login_view = 'main.login'
  # Import and register the routes
  from app import models
  with app.app_context():
    db.create_all()
  from app.routes import main_routes
  app.register_blueprint(main_routes)
  
  # Handle errors
  from app.errors import register_error_handlers
  register_error_handlers(app)
  
  return app
  
  
  
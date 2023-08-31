from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.instance.config import app_config

# Create SQLAlchemy and Migrate instances
database = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=app_config):
    # Create the Flask application instance
    application = Flask(__name__)
    
    # Load configuration from the provided config class
    application.config.from_object(config_class)

    # Initialize database and migrations
    database.init_app(application)
    migrate.init_app(app=application, 
                     db=database, 
                     directory="intron_health_migrations",
                     render_as_batch=True)

    with application.app_context():
        # Import and register all Blueprints
        from .home import home as home_blueprint
        application.register_blueprint(home_blueprint, url_prefix="/home")

    return application

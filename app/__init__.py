from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import google.generativeai as genai
import nest_asyncio

# Apply nest_asyncio to allow running asyncio code within Flask
nest_asyncio.apply()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Por favor, inicia sesión para acceder a esta página.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Configure Gemini
    try:
        api_key = app.config['GEMINI_API_KEY']
        if not api_key or 'your_gemini_api_key' in api_key:
            app.logger.warning("GEMINI_API_KEY is not set or is set to the default value. Scraping will fail.")
        else:
            genai.configure(api_key=api_key)
            app.logger.info("Gemini API Key configured.")
    except Exception as e:
        app.logger.error(f"Error configuring Gemini API Key: {e}")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

from app import models 
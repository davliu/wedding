# -*- coding: utf-8 -*-

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import configs

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    register_blueprints(app)
    app.config.from_object(configs["default"])
    app.config.from_pyfile("config.py", silent=True)
    csrf.init_app(app)
    return app

def register_blueprints(app):
    with app.app_context():
        from app.pages.controllers import bp as pages_bp
        app.register_blueprint(pages_bp)

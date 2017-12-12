# -*- coding: utf-8 -*-

from flask import Flask
from config import configs

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    register_blueprints(app)
    app.config.from_object(configs["default"])
    app.config.from_pyfile("config.py", silent=True)
    return app

def register_blueprints(app):
    with app.app_context():
        from app.pages.controllers import bp as pages_bp
        app.register_blueprint(pages_bp)

# -*- coding: utf-8 -*-

from flask import Flask

def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

def register_blueprints(app):
    with app.app_context():
        from app.pages.controllers import bp as pages_bp
        app.register_blueprint(pages_bp)

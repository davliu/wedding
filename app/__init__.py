# -*- coding: utf-8 -*-

from flask import Flask, url_for, request
from flask_wtf.csrf import CSRFProtect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import configs

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    register_blueprints(app)
    app.config.from_object(configs["default"])
    app.config.from_pyfile("config.py", silent=True)
    csrf.init_app(app)

    # Init spotipy client
    spotipy_creds = SpotifyClientCredentials(
        client_id=app.config["SPOTIPY_CLIENT_ID"],
        client_secret=app.config["SPOTIPY_CLIENT_SECRET"],
    )
    app.spotipy_client = spotipy.Spotify(client_credentials_manager=spotipy_creds)

    @app.context_processor
    def inject_nav():
        nav_items = [
            dict(title="Home", route=url_for("pages.index")),
            dict(title="Our Story", route=url_for("pages.story")),
            dict(title="Event Info", route=url_for("pages.event")),
            dict(title="RSVP", route=url_for("pages.rsvp")),
        ]
        for nav_item in nav_items:
            nav_item["disabled"] = request.path == nav_item["route"]
        return dict(nav_items=nav_items)

    return app

def register_blueprints(app):
    with app.app_context():
        from app.pages.controllers import bp as pages_bp
        app.register_blueprint(pages_bp)

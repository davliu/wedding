# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint("pages", __name__)

@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/index.html")

@bp.route("/our-story", methods=["GET"])
def story():
    return render_template("pages/our-story.html")

@bp.route("/event-info", methods=["GET"])
def event():
    return render_template("pages/event-info.html")

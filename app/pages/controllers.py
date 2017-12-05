# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint("pages", __name__)

@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/index.html")

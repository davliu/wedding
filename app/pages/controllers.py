# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for

from app.pages.forms import RSVPForm
from app.pages.rsvp_models import RSVP

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

@bp.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    if request.method == "POST":
        form = RSVPForm()
        if form.validate_on_submit():
            if RSVP.reserve(form):
                flash("Thank you for registering!")
                return redirect(url_for("pages.index"))
            else:
                flash("Please double check your info and try again!")
    else:
        form = RSVPForm()
    return render_template("pages/rsvp.html", form=form)

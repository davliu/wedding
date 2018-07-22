# -*- coding: utf-8 -*-

import copy

from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
)

from app.pages.forms import RSVPForm, RSVPUpdateForm
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
    flash(
        "The RSVP period is over! "
        "Please contact us at davidjanetliu@gmail.com for any questions.")
    return redirect(url_for("pages.index"))

    session.pop("invite", None)
    form = RSVPForm()
    if request.method == "POST":
        if form.validate_on_submit():
            invite = RSVP.validate_invitation_code(form)
            if invite:
                session["invite"] = invite
                return redirect(url_for("pages.rsvp_update"))
    else:
        form = RSVPForm()
    return render_template("pages/rsvp.html", form=form)

@bp.route("/rsvp/update", methods=["GET", "POST"])
def rsvp_update():
    invite = session.get("invite")
    if not invite:
        if request.method == "POST":
            flash("Session expired. Please try again!")
        return redirect(url_for("pages.rsvp"))

    # Populate form fields
    form = RSVPUpdateForm()
    if request.method == "GET":
        RSVP.populate_invite(form, invite)

    return_invite = copy.copy(invite)
    return_invite.pop("row", None)
    if request.method == "POST":
        if invite["invitation_code"] != form.invitation_code.data:
            flash("Mismatching reservation! Please try to RSVP again.")
            return redirect(url_for("pages.rsvp"))

        if form.validate_on_submit() and RSVP.reserve(form, invite):
            session.pop("invite", None)
            flash("Thank you for registering!")
            return redirect(url_for("pages.index"))
    return render_template("pages/rsvp_update.html", form=form, invite=return_invite)

@bp.route("/track_search", methods=["GET"])
def track_search():
    query = request.args.get("q")
    if not query:
        return jsonify(tracks=[])

    if "*" not in query:
        query = u"{}*".format(query)
    json_tracks = current_app.spotipy_client.search(q=query, type="track", limit=5)
    tracks = [
        u"{} by {}".format(
            i["name"],
            u" and ".join([a["name"] for a in i["artists"]]) if len(i["artists"]) <= 2 else
            u" and ".join([a["name"] for a in i["artists"][:2]] + ["etc."])
        ) for i in json_tracks["tracks"]["items"]
    ]
    return jsonify(tracks=tracks)

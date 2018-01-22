# -*- coding: utf-8 -*-

import copy

from flask import Blueprint, render_template, request, flash, redirect, url_for, session

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
        for k, v in invite.iteritems():
            try:
                if not getattr(form, k).data:
                    getattr(form, k).data = v
            except:
                pass

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

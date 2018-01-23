# -*- coding: utf-8 -*-
from datetime import datetime
import json
import pytz

from flask import current_app
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from wtforms import BooleanField

RETRIEVE_FIELDS = {
    "attending",
    "person",
    "invitation_code",
    "plus_one",
    "email",
    "vegetarian",
    "plus_one",
    "plus_one_name",
    "plus_one_vegetarian",
    "additional_comments",
    "song_suggestion_1",
    "song_suggestion_2",
    "song_suggestion_3",
}

UPDATE_FIELDS = {
    "attending",
    "vegetarian",
    "plus_one",
    "plus_one_name",
    "plus_one_vegetarian",
    "additional_comments",
    "song_suggestion_1",
    "song_suggestion_2",
    "song_suggestion_3",
}

class RSVP(object):
    @staticmethod
    def get_wks():
        scope = ['https://spreadsheets.google.com/feeds']

        with current_app.open_instance_resource('service-credentials.json') as f:
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.load(f), scope)

        gc = gspread.authorize(credentials)
        try:
            return (
                gc.
                open(current_app.config["SPREADSHEET_NAME"]).
                worksheet(current_app.config["SHEET_TAB_NAME"])
            )
        except:
            return

    @staticmethod
    def get_headers(wks):
        return {v.replace(" ", "_").lower(): k for k, v in enumerate(wks.row_values(1)) if v}

    @staticmethod
    def populate_invite(form, invite):
        for k, v in invite.iteritems():
            try:
                field = getattr(form, k)
                field.data = bool(int(v or 0)) if type(field) == BooleanField else v
            except:
                pass

    @staticmethod
    def validate_invitation_code(form):
        wks = RSVP.get_wks()
        try:
            matching_cell = wks.find(form.invitation_code.data.upper())
        except:
            matching_cell = None
        if not matching_cell:
            form.invitation_code.errors.append("Double check your invitation code and try again.")
            return

        headers = RSVP.get_headers(wks)
        row_values = wks.row_values(matching_cell.row)
        invite = {
            h: row_values[i]
            for h, i in headers.iteritems() if h in RETRIEVE_FIELDS
        }
        invite["row"] = matching_cell.row
        return invite

    @staticmethod
    def reserve(form, invite):
        wks = RSVP.get_wks()
        headers = RSVP.get_headers(wks)

        # Update cells
        for field, value in form.data.items():
            if field not in UPDATE_FIELDS:
                continue
            save_value = value
            if type(value) == bool:
                save_value = 1 if value else 0
            wks.update_cell(invite["row"], headers[field] + 1, save_value)

        time_now = pytz.utc.localize(
            datetime.utcnow()).astimezone(pytz.timezone("America/Los_Angeles"))
        wks.update_cell(
            invite["row"], headers["rsvp_time"] + 1, time_now.strftime("%Y-%m-%dT%H:%M:%S PST"))
        return True

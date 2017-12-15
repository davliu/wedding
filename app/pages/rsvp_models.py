# -*- coding: utf-8 -*-
from datetime import datetime
import json
import pytz
import re

from flask import current_app
import gspread
from oauth2client.service_account import ServiceAccountCredentials

UPDATE_FIELDS = [
    "plus_one",
    "plus_one_first_name",
    "plus_one_last_name",
    "vegetarian",
]

class RSVP(object):
    @staticmethod
    def get_headers(wks):
        return {v.replace(" ", "_").lower(): k + 1 for k, v in enumerate(wks.row_values(1)) if v}

    @staticmethod
    def reserve(form):
        scope = ['https://spreadsheets.google.com/feeds']

        with current_app.open_instance_resource('service-credentials.json') as f:
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.load(f), scope)

        gc = gspread.authorize(credentials)
        try:
            wks = (
                gc.
                open(current_app.config["SPREADSHEET_NAME"]).
                worksheet(current_app.config["SHEET_TAB_NAME"])
            )
        except:
            return False

        re_compile = re.compile(
            r"^({}).*({})$".format(
                form.first_name.data.split(" ")[0],
                form.last_name.data.split(" ")[-1]
            ), re.IGNORECASE)
        try:
            matching_cell = wks.find(re_compile)
        except:
            return False

        headers = RSVP.get_headers(wks)

        # Check if passcode match
        if (
            (wks.cell(matching_cell.row, headers["passcode"]).value or "").lower().strip() !=
            (form.passcode.data or "").lower().strip()
        ):
            return False

        # Update cells
        for field, value in form.data.items():
            if not value or field not in UPDATE_FIELDS:
                continue
            save_value = value
            if type(value) == bool:
                save_value = 1 if value else 0
            wks.update_cell(matching_cell.row, headers[field], save_value)

        time_now = pytz.utc.localize(
            datetime.utcnow()).astimezone(pytz.timezone("America/Los_Angeles"))
        wks.update_cell(
            matching_cell.row, headers["rsvp_time"], time_now.strftime("%Y-%m-%dT%H:%M:%S PST"))
        return True

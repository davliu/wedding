# -*- coding: utf-8 -*-
import argparse
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from flask import render_template

from app.pages.rsvp_models import RSVP

"""
For Avery 15661 labels
"""

def generate_html(offset=None):
    offset = offset or 0
    my_app = create_app()
    with my_app.app_context():
        wks = RSVP.get_wks()
        headers = RSVP.get_headers(wks)
        names = wks.col_values(headers["person"] + 1)[offset:]
        invitation_codes = wks.col_values(headers["invitation_code"] + 1)[offset:]
        invites = [dict(name=name, code=invitation_codes[i]) for i, name in enumerate(names) if name]
        template = render_template("labels.html", invites=invites)
        with open("scripts/my_template.html", "w+") as myf:
            myf.write(template)
        return template


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--offset", help="Offset")

    args = parser.parse_args()
    generate_html(offset=args.offset or 0)

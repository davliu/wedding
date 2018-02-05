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

def format_address(address):
    comma_index = address.index(",")
    return [address[:comma_index], address[comma_index + 1:].strip()]

def generate_html(offset=None, use_addresses=None, blanks=None):
    offset = offset or 0
    blanks = blanks or 0

    my_app = create_app()
    with my_app.app_context():
        wks = RSVP.get_wks()
        headers = RSVP.get_headers(wks)
        names = wks.col_values(headers["person"] + 1)[offset:]
        if not use_addresses:
            invitation_codes = wks.col_values(headers["invitation_code"] + 1)[offset:]
            invites = [
                dict(name=name, code=invitation_codes[i]) for i, name in enumerate(names) if name]
        else:
            addresses = wks.col_values(headers["address"] + 1)[offset:]
            invites = [
                dict(name=name, address=format_address(addresses[i]))
                for i, name in enumerate(names)
                if name and addresses[i] and addresses[i] != "HAND DELIVERED"
            ]

        if blanks:
            invites = [dict(name="", code="", address="") for _ in range(blanks)] + invites
        template = render_template("labels.html", invites=invites, use_addresses=use_addresses)
        with open("scripts/my_template.html", "w+") as myf:
            myf.write(template)
        return template


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--offset", help="Offset")
    parser.add_argument("-a", "--addresses", help="Generate address labels") # Invite codes defaulted
    parser.add_argument("-b", "--blanks", help="Initial blanks") # When printing partial sheets

    args = parser.parse_args()
    generate_html(
        offset=int(args.offset or 0),
        use_addresses=bool(args.addresses),
        blanks=int(args.blanks or 0),
    )

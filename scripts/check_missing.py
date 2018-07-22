# -*- coding: utf-8 -*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from app import create_app
from app.pages.rsvp_models import RSVP

def get_people():
    my_app = create_app()
    with my_app.app_context():
        # Get RSVP'd names
        wks = RSVP.get_wks()
        headers = RSVP.get_headers(wks)
        wks = RSVP.get_wks()
        names = [n.lower() for n in wks.col_values(headers["person"] + 1)[1:] if n]
        plus_one_names = [n.lower() for n in wks.col_values(headers["plus_one_name"] + 1)[1:] if n]
        rsvpd_names = set(names) | set(plus_one_names)

        # Get seating chart names
        seating_sheet = RSVP.get_wks(sheet_tab_name="Seating")
        i = 1
        table_names = []
        while True:
            new_names = [
                (i, n) for n in seating_sheet.col_values(i)[1:]
                if n and not n.isdigit() and n != "Total Guest Count"]
            i += 1
            if not new_names:
                break
            table_names.extend(new_names)

        seating_names = {n[1].lower() for n in table_names}
        # missing_names = seating_names ^ rsvpd_names
        # print "Missing Names:"
        # print json.dumps(list(missing_names), indent=4)
        print "Missing in Seating Chart:"
        print json.dumps(list(rsvpd_names - seating_names), indent=4)
        print "In Seating Chart, but not Guest List:"
        print json.dumps(list(seating_names - rsvpd_names), indent=4)

        print "Attending:"
        formatted_names = []
        for table_name in table_names:
            table_name_split = table_name[1].replace("(Veg)", "").strip().split(" ")
            formatted_names.append((
                table_name[0],
                u"{}, {}".format(table_name_split[-1], " ".join(table_name_split[:-1]))))
        formatted_names = sorted(formatted_names, key=lambda e: e[1])
        for formatted_name in formatted_names:
            print formatted_name[0]
        for formatted_name in formatted_names:
            print formatted_name[1]


if __name__ == "__main__":
    get_people()

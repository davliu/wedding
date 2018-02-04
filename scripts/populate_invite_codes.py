# -*- coding: utf-8 -*-
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from random import random

from app import create_app
from app.pages.rsvp_models import RSVP

CODE_LENGTH = 5

def generate_code():
    valid_chars = [chr(i) for i in range(65, 65 + 26)] + [unicode(i) for i in range(10)]
    return u"".join([valid_chars[int(random() * len(valid_chars))] for _ in range(CODE_LENGTH)])

def populate_codes():
    my_app = create_app()
    with my_app.app_context():
        wks = RSVP.get_wks()
        headers = RSVP.get_headers(wks)
        name_col = headers["person"] + 1
        code_col = headers["invitation_code"] + 1

        curr_row = 1
        while wks.cell(curr_row, name_col).value:
            invite_code = wks.cell(curr_row, code_col).value
            if not invite_code:
                wks.update_cell(curr_row, code_col, generate_code())
            curr_row += 1


if __name__ == "__main__":
    populate_codes()

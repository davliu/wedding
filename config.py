# -*- coding: utf-8 -*-
import subprocess

class Config(object):
    GOOGLE_BROWSER_KEY = "<API_KEY_HERE>"
    SECRET_KEY = "SUPER_SECRET"
    SPREADSHEET_NAME = "MY_SPREADSHEET_NAME"
    SHEET_TAB_NAME = "MY_TAB_NAME"
    TEMPLATES_AUTO_RELOAD = True
    GIT_REV_HASH = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()


configs = {
    "default": Config
}

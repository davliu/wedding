#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app
from flask_script import Manager

app = create_app()
manager = Manager(app)

@manager.command
def runserver(sync=False):
    app.run(debug=True, port=5001, threaded=not sync, host="0.0.0.0")


if __name__ == "__main__":
    manager.run()

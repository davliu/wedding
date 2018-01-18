# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Regexp

class RSVPForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(message="Your first name is required"),
            Regexp(r"^[A-z \d]*$", message="No record of this name"),
        ],
        render_kw={"placeholder": "First Name"},
    )
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(message="Your last name is required"),
            Regexp(r"^[A-z \d]*$", message="No record of this name"),
        ],
        render_kw={"placeholder": "Last Name"},
    )
    plus_one = BooleanField("Plus One?")
    plus_one_name = StringField(
        "Plus One Name (First and Last)",
        validators=[Regexp(r"^[A-z \d]*$", message="No record of this name")],
        render_kw={"placeholder": "Plus One Name"},
    )
    passcode = StringField(
        "Passcode",
        validators=[DataRequired(message="Enter the passcode included in your invite")],
        render_kw={"placeholder": "Invitation Code"},
    )
    vegetarian = BooleanField("Vegetarian?")
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Solve the recaptcha correctly!")])
    plus_one_vegetarian = BooleanField("Vegetarian?")

    def validate(self):
        valid = FlaskForm.validate(self)
        if self.plus_one.data:
            if not self.plus_one_name.data:
                self.plus_one_name.errors.append("What is this person's name?")
                valid = False

        if not valid:
            return False

        return True

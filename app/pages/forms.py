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
        ]
    )
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(message="Your last name is required"),
            Regexp(r"^[A-z \d]*$", message="No record of this name"),
        ]
    )
    plus_one = BooleanField("Plus One?")
    plus_one_first_name = StringField(
        "Plus First Name",
        validators=[Regexp(r"^[A-z \d]*$", message="No record of this name")],
    )
    plus_one_last_name = StringField(
        "Plus Last Name",
        validators=[Regexp(r"^[A-z \d]*$", message="No record of this name")],
    )
    passcode = StringField(
        "Passcode", validators=[DataRequired(message="Enter the passcode included in your invite")])
    vegetarian = BooleanField("Vegetarian?")
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Solve the recaptcha correctly!")])

    def validate(self):
        valid = FlaskForm.validate(self)
        if self.plus_one.data:
            if not self.plus_one_first_name.data:
                self.plus_one_first_name.errors.append("What is this person's first name?")
                valid = False
            if not self.plus_one_last_name.data:
                self.plus_one_last_name.errors.append("What is this person's last name?")
                valid = False

        if not valid:
            return False

        return True

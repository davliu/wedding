# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Regexp, length

class RSVPForm(FlaskForm):
    invitation_code = StringField(
        "Invitation Code (found in your invite)",
        validators=[
            DataRequired(message="Enter the invitation code included in your invite"),
            Regexp(r"^[A-z0-9]+$", message="No special characters allowed"),
            length(max=4),
        ],
        render_kw={"placeholder": "Invitation Code"},
    )
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Solve the recaptcha correctly!")])

class RSVPUpdateForm(FlaskForm):
    invitation_code = StringField(
        "Invitation Code (found in your invite)",
        validators=[
            DataRequired(message="Enter the invitation code included in your invite"),
            Regexp(r"^[A-z0-9]+$", message="No special characters allowed"),
            length(max=4),
        ],
        render_kw={"placeholder": "Invitation Code"},
    )

    plus_one = BooleanField("Plus One?")
    plus_one_name = StringField(
        "Plus One Name (First and Last)",
        validators=[
            Regexp(r"^[A-z \d\']*$", message="No special characters allowed"),
            length(max=200),
        ],
        render_kw={"placeholder": "Plus One Name"},
    )
    vegetarian = BooleanField("Vegetarian?")
    plus_one_vegetarian = BooleanField("Vegetarian?")
    additional_comments = TextAreaField(
        "Additional Comments",
        validators=[length(max=200)],
    )

    def validate(self):
        valid = FlaskForm.validate(self)
        if self.plus_one.data:
            if not self.plus_one_name.data:
                self.plus_one_name.errors.append("What is this person's name?")
                valid = False

        if not valid:
            return False

        return True

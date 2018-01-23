# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, BooleanField, TextAreaField, HiddenField
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
    invitation_code = HiddenField("Invitation Code (found in your invite)")
    attending = BooleanField("Will you be attending?")
    plus_one = BooleanField("Are you bringing a plus one?")
    plus_one_name = StringField(
        "Plus One Name (First and Last)",
        validators=[
            Regexp(r"^[A-z \d\']*$", message="No special characters allowed"),
            length(max=200),
        ],
        render_kw={"placeholder": "Plus One Name"},
    )
    vegetarian = BooleanField("Are you vegetarian?")
    plus_one_vegetarian = BooleanField("Is your plus-one vegetarian?")
    additional_comments = TextAreaField(
        "Additional Comments",
        validators=[length(max=200)],
    )
    song_suggestion_1 = StringField(
        "Song Suggestion 1",
        validators=[length(max=100)], render_kw={"placeholder": "Optional"},
    )
    song_suggestion_2 = StringField(
        "Song Suggestion 2",
        validators=[length(max=100)], render_kw={"placeholder": "Optional"},
    )
    song_suggestion_3 = StringField(
        "Song Suggestion 3",
        validators=[length(max=100)], render_kw={"placeholder": "Optional"},
    )

    def validate(self):
        valid = FlaskForm.validate(self)
        if self.plus_one.data:
            if not self.plus_one_name.data:
                self.plus_one_name.errors.append("What is this person's name?")
                valid = False
        else:
            self.plus_one_name.data = ""
            self.plus_one_vegetarian.data = False

        if not valid:
            return False

        return True

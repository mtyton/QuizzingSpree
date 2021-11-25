from wtforms import (
    Form, BooleanField, StringField, PasswordField,
    validators
)


class RegistrationForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField("Email Address", [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired,
        validators.EqualTo('confirm', message="Password must match")
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField(
        "I accept Terms Of Use", [validators.DataRequired()]
    )

    def save(self):
        if not self.data:
            return


from wtforms import (
    Form, BooleanField, StringField, PasswordField,
    validators
)
from werkzeug.security import check_password_hash

from apps.auth.models import User


class RegistrationForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField("Email Address", [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Password must match")
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField(
        "I accept Terms Of Use", [validators.DataRequired()]
    )

    def save(self):
        if not self.data:
            return


class LoginForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired()
    ])
    remember_me = BooleanField("Remember Me")

    _user_instance = None

    @property
    def user_instance(self):
        if not self._user_instance:
            username = self.data.get('username')
            self._user_instance = User.query.filter_by(
                username=username
            ).first()
        return self._user_instance

    def validate(self, extra_validators=None) -> bool:
        valid = super().validate(extra_validators)
        user = self.user_instance
        password = self.data.get('password')

        if not user:
            return False

        # validate password
        return valid & check_password_hash(user.password, password)

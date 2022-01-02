from typing import Union
from wtforms import (
    Form, BooleanField, StringField, PasswordField,
    validators
)
from werkzeug.security import check_password_hash

from apps.auth.models import User
from database.database import db


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

    def __check_password_match(self) -> bool:
        return (
            self.data.get('password') == self.data.get('confirm')
            and self.data.get('password') is not None
        )

    def __check_if_user_already_exists(self) -> bool:
        user = User.query.filter_by(email=self.data.get('email')).first()
        if user:
            return True
        # TODO add proper form errors
        user = User.query.filter_by(username=self.data.get('username')).first()
        return user is not None

    def validate(self, extra_validators=None) -> bool:
        valid = super().validate(extra_validators)
        # check if there exists such a user
        if self.__check_if_user_already_exists():
            return False
        # check if password match
        if not self.__check_password_match():
            self.form_errors
            return False

        return valid

    # TODO - implement method which will notify user about his registration
    def __send_registration_email(self) -> int:
        pass

    def save(self) -> Union[User, None]:
        if not self.data:
            return
        if not self.validate():
            return

        user_data = {
            'username': self.data.get('username'),
            'email': self.data.get('email'),
            'password': self.data.get('password')
        }
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user


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

from flask.typing import ResponseReturnValue
from flask import (
    render_template, Blueprint, redirect, url_for, request, flash
)
from flask_login import current_user, login_user, logout_user
from flask.views import MethodView

from apps.base.views import BasePermissionCheckMethodView
from apps.auth.forms import RegistrationForm, LoginForm
from apps.auth.permissions import (
    IsAuthenticatedPermission, IsNotAuthenticatedPermission
)


bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginView(BasePermissionCheckMethodView):
    methods = ["GET", "POST"]
    template_name = "auth/login.html"

    permissions = [IsNotAuthenticatedPermission(), ]

    def get_context(self) -> dict:
        return {
            'form': LoginForm()
        }

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            user = form.user_instance
            login_user(user)
            return redirect(url_for('auth.my_account'), code=301)

        flash("No such user or incorrect_password", "error")
        return self.get()


class LogoutView(BasePermissionCheckMethodView):
    methods = ["GET"]
    template_name = "auth/logout.html"

    permissions = [IsAuthenticatedPermission(), ]

    def get(self):
        logout_user()
        return redirect(url_for('home'), code=302)


class RegisterView(BasePermissionCheckMethodView):
    methods = ["GET", "POST"]
    template_name = "auth/register.html"

    permissions = [IsNotAuthenticatedPermission(), ]

    def get_context(self) -> dict:
        return {
            'form': RegistrationForm()
        }

    def post(self):
        form = RegistrationForm(request.form)
        user = form.save()
        if not user:
            flash("Something went wrong", "error")
            return render_template(self.template_name, **{'form': form})

        # after creating an account automatically login user
        login_user(user)
        return redirect(url_for('auth.my_account'), code=201)


class MyAccountView(BasePermissionCheckMethodView):
    methods = ["GET"]
    template_name = "auth/account.html"

    permissions = [IsAuthenticatedPermission(), ]


bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
bp.add_url_rule('/register', view_func=RegisterView.as_view('register'))
bp.add_url_rule('/account', view_func=MyAccountView.as_view('my_account'))

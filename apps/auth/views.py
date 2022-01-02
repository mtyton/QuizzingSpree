from flask.typing import ResponseReturnValue
from flask import (
    render_template, Blueprint, redirect, url_for, request, flash
)
from flask_login import current_user, login_user, logout_user, login_required
from flask.views import View, MethodView


from apps.auth.forms import RegistrationForm, LoginForm


bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginView(MethodView):
    methods = ["GET", "POST"]
    template_name = "auth/login.html"

    def get_context(self) -> dict:
        return {
            'form': LoginForm()
        }

    def get(self):
        return render_template(self.template_name, **self.get_context())

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            user = form.user_instance
            login_user(user)
            return redirect(url_for('auth.my_account'), code=302)

        flash("No such user or incorrect_password", "error")
        return self.get()


class LogoutView(MethodView):
    methods = ["GET"]
    template_name = "auth/logout.html"

    @login_required
    def get(self):
        logout_user()
        # TODO - should redirect into index page
        return redirect(url_for('auth.register'), code=302)


class RegisterView(MethodView):
    methods = ["GET", "POST"]
    template_name = "auth/register.html"

    def get_context(self) -> dict:
        return {
            'form': RegistrationForm()
        }

    def get(self):
        # TODO - registered user should be redirected to my-account
        if current_user.is_authenticated:
            return redirect(url_for('auth.my_account'), code=302)

        return render_template(self.template_name, **self.get_context())


class MyAccountView(MethodView):
    methods = ["GET"]

    def get(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.register'), code=302)

        return render_template("auth/account.html")


bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
bp.add_url_rule('/register', view_func=RegisterView.as_view('register'))
bp.add_url_rule('/account', view_func=MyAccountView.as_view('my_account'))

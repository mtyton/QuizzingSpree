from flask_login.login_manager import LoginManager

from apps.auth.models import User

login_manager = LoginManager()


def configure_login_manager(app):
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from flask_login import current_user


def logged_user():
    return {'current_user': current_user}

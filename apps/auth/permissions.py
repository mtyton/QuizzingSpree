from flask_login import current_user


class IsAuthenticatedPermission:

    def check_permission(self):
        if current_user.is_authenticated:
            return True
        return False


class IsNotAuthenticatedPermission:

    def check_permission(self):
        if current_user.is_authenticated:
            return False
        return True


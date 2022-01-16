from apps.base.tests.test_base import test_app


# TODO - create login context manager
def login(test_app, username, password):
    return test_app.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(test_app):
    return test_app.get('/auth/logout', follow_redirects=True)

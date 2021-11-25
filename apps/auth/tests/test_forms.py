from apps.auth.forms import RegistrationForm
from apps.auth.models import User


class TestClassRegistrationForm:

    def test_save_success(self):
        registration_data = {
            'username': "John Doe",
            'email': "john.doe@mtyton.com",
            'password': "ThisIsC@mplexP@ssword",
            'confirm': "ThisIsC@mplexP@ssword",
            'accept_tos': True
        }
        form = RegistrationForm(formdata=registration_data)
        assert form.validate() is True
        # save form entrance
        form.save()
        users = User.query.filter(username=registration_data['username']).all()
        assert len(users) == 1
        assert users.first.email == registration_data['email']

    def test_save_user_already_exists(self):
        registration_data = {
            'username': "John Doe",
            'email': "john.doe@mtyton.com",
            'password': "ThisIsC@mplexP@ssword",
            'confirm': "ThisIsC@mplexP@ssword",
            'accept_tos': True
        }
        form = RegistrationForm(formdata=registration_data)
        assert form.validate() is True
        # save form entrance
        form.save()
        users = User.query.filter(username=registration_data['username']).all()
        assert len(users) == 1
        assert users.first.email == registration_data['email']


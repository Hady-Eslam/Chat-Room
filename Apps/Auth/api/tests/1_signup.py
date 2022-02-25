from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion,
    helper.GetMethodNotAllowed, helper.PostInvalidData
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Signup',
            URL=reverse('Auth.api:Signup'),
            Host=os.environ.get('HOST')
        )

    def test_username_exists(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, data={
            'email': os.environ.get('TEST_USER_EMAIL'),
            'username': os.environ.get('SUPER_USER_USERNAME'),
            'password': '000'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 400, self._Message('UserName Exists'))

    def test_create_user(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, data={
            'email': os.environ.get('TEST_USER_EMAIL'),
            'username': os.environ.get('TEST_USER_USERNAME'),
            'password': os.environ.get('TEST_USER_PASSWORD')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 201, self._Message('Create User'))

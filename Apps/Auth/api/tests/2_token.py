from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os




class TestApi(SimpleTestCase, helper.TestAPIHelper, helper.GetMethodNotAllowed, helper.PostInvalidData):

    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Token',
            URL=reverse('Auth.api:Token'),
            Host=os.environ.get('HOST')
        )
        
    def test_wrong_username(self):

        _response = requests.post(self._url, data={
            'username': 'adasd',
            'password': '000'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 401, self._Message('Wrong UserName'))

    def test_wrong_password(self):

        _response = requests.post(self._url, data={
            'username': os.environ.get('SUPER_USER_USERNAME'),
            'password': '000'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 401, self._Message('Wrong Password'))

    def test_user_not_active(self):

        _response = requests.post(self._url, data={
            'username': os.environ.get('TEST_USER_USERNAME'),
            'password': os.environ.get('TEST_USER_PASSWORD')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 401, self._Message('User is Not Active'))

    def test_get_token(self):

        _response = requests.post(self._url, data={
            'username': os.environ.get('SUPER_USER_USERNAME'),
            'password': os.environ.get('SUPER_USER_PASSWORD')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Get Token'))

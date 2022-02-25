import requests, os
from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion,
    helper.GetMethodNotAllowed, helper.PostInvalidData
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Forget Password',
            URL=reverse('Auth.api:Forget-Password'),
            Host=os.environ.get('HOST')
        )
    
    def test_username_does_not_exists(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, data={
            'username': 'username'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('UserName Does Not Exists Exists'))
    

    def test_guest_user(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, data={
            'username': os.environ.get('GUEST_USERNAME')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('UserName Does Not Exists Exists'))

    def test_user_not_active(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, data={
            'username': os.environ.get('TEST_USER_USERNAME')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('User Not Active'))

    def test_forget_password(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, data={
            'username': os.environ.get('SUPER_USER_USERNAME'),
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Forget Password'))

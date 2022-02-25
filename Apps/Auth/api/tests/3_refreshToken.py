from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestApi(SimpleTestCase, helper.TestAPIHelper, helper.GetMethodNotAllowed, helper.PostInvalidData):

    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Refresh Token',
            URL=reverse('Auth.api:Refresh'),
            Host=os.environ.get('HOST')
        )
    
    def test_invalid_refresh(self):

        _response = requests.post(self._url, data={
            'refresh': 'adasd'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 401, self._Message('Invalid Refresh Token'))
    
    def test_get_refresh_token(self):

        self._Authorize()

        _response = requests.post(self._url, data={
            'refresh': self._Refresh
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Get Refresh Token'))

from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion,
    helper.TokenNotInQuery, helper.TokenNotFound
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Get Reset Password',
            URL=reverse('Auth.api:Reset-Password'),
            Host=os.environ.get('HOST')
        )
    
    def test_not_user_token(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1'
        }, params={
            'Token': 'UWKWDkJRYljg4Qey7oIJEpG3A0X0hhk-nU4OSFsYkHbZRRB-r7yhP35a9OJKnHbDSMqpvZ7Fwgdx6Z6ugMdP'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Not User Token'))
    
    def test_token_found(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1'
        }, params={
            'Token': '_xKa6mVj_Knz6yT9y_EmizG_LMPRqM2St8K0Jo12TtRogFXDXEsRYua62OL_2Q1-yEM'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Token Found'))

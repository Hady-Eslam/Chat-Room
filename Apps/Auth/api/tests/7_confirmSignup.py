from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion,
    helper.PostTokenNotInQuery, helper.PostTokenNotFound
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Confirm Signup',
            URL=reverse('Auth.api:Confirm-Signup'),
            Host=os.environ.get('HOST')
        )
    
    def test_not_user_token(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, params={
            'Token': 'Op6p4hkb9qWNVFEGqe21bb5KPar38-QxEPk84zm0oEHqTZY1evKkrSoYqYomY8SRu7n5Ergo-eRb'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Not User Token'))
    
    def test_confirm_signup(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, params={
            'Token': 'W4H3597LqI6hmBXPPn-epUiLSbuy_Gza7dJRupedMoSTiG6buAxtpGXuTG9rn4jSajyIIA'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Confirm Signup'))

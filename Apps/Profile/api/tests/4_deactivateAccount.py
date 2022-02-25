from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PostMethodNotAllowed
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Deactivate Account',
            URL=reverse('Profile.api:Profile'),
            Host=os.environ.get('HOST')
        )
        self._Authorize()


    def test_deactivate_guest_user(self):

        self._Authorize(os.environ.get('GUEST_USERNAME'), os.environ.get('GUEST_PASSWORD'))

        _response = requests.delete(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 403, self._Message('Deactivate Guest User'))
    

    def test_deactivate_superuser_user(self):

        _response = requests.delete(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 403, self._Message('Deactivate SuperUser'))


    def test_deactivate_account(self):

        self._Authorize(os.environ.get('TEST_USER_USERNAME'), os.environ.get('TEST_USER_PASSWORD'))

        _response = requests.delete(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 204, self._Message('Deactivate Test User'))

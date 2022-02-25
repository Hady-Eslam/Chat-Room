from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PostMethodNotAllowed, helper.PatchInvalidData
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Update Password',
            URL=reverse('Profile.api:Password'),
            Host=os.environ.get('HOST')
        )
        self._Authorize()


    def test_update_password(self):

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data={
            'password': os.environ.get('SUPER_USER_PASSWORD')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update Password'))

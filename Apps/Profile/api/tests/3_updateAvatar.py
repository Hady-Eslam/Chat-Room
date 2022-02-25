from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PostMethodNotAllowed, 
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Update Profile',
            URL=reverse('Profile.api:Avatar'),
            Host=os.environ.get('HOST')
        )
        self._Authorize()

    
    def test_update_profile_avatar(self):

        _response = requests.api.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, files={
            'avatar': open(os.environ.get('TEST_USER_AVATAR'), 'rb')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update User Profile Avatar'))

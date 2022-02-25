from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestAPI(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PatchMethodNotAllowed, helper.PostInvalidData
):
    def setUp(self) -> None:
        self._setUp(
            Production=False,
            API_Name='Create Chat Room',
            URL=reverse('Chat.api:Rooms'),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    

    def test_create_room(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data={
            'name': 'Test API Room',
            'password': os.environ.get('TEST_ROOM_PASSWORD'),
            'description': 'This is Test Description'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 201, self._Message('Create Chat Room'))

from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestAPI(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PostMethodNotAllowed, helper.PatchInvalidData, helper.PatchRoomNotFound
):
    def setUp(self) -> None:
        self._setUp(
            Production=False,
            API_Name='Join Room',
            URL=reverse('Chat.api:Join-Room', kwargs={
                'Room_Code': '--Idci9VGC7DTbOsKaodrw'
            }),
            URL_Not_Found=reverse('Chat.api:Join-Room', kwargs={
                'Room_Code': 'zH3lxyoMMc-V4w7xOchnerpDEfsjS7DsL1dAGGo'
            }),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    

    def test_wrong_password(self):

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data={
            'password': os.environ.get('TEST_ROOM_PASSWORD') + 'afdfdsfds',
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 403, self._Message('Wrong Password'))
    

    def test_already_member(self):

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data={
            'password': os.environ.get('TEST_ROOM_PASSWORD'),
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Already Room Member'))
    

    def test_join_room(self):

        self._Authorize(os.environ.get('GUEST_USERNAME'), os.environ.get('GUEST_PASSWORD'))

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data={
            'password': os.environ.get('TEST_ROOM_PASSWORD'),
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Join Room'))

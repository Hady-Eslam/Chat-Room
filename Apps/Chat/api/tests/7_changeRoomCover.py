from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestAPI(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.GetMethodNotAllowed, helper.PatchRoomNotFound
):
    def setUp(self) -> None:
        self._setUp(
            Production=False,
            API_Name='Change Room Cover',
            URL=reverse('Chat.api:Cover-Settings', kwargs={
                'Room_Code': 'zH3l37Hn96ZkxyoMMc-V4w7xOchnerpDEfsjS7DsL1dAGGo'
            }),
            URL_Not_Found=reverse('Chat.api:Cover-Settings', kwargs={
                'Room_Code': 'zH3lxyoMMc-V4w7xOchnerpDEfsjS7DsL1dAGGo'
            }),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    

    def test_not_admin(self):
        
        self._Authorize(os.environ.get('GUEST_USERNAME'), os.environ.get('GUEST_PASSWORD'))

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 403, self._Message('Not Admin'))
    

    def test_update_room_cover(self):

        _response = requests.api.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, files={
            'cover': open(os.environ.get('TEST_ROOM_COVER'), 'rb')
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update Room Cover'))

from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestAPI(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PostMethodNotAllowed, helper.GetRoomNotFound
):
    def setUp(self) -> None:
        self._setUp(
            Production=False,
            API_Name='Get Member Info',
            URL=reverse('Chat.api:Member', kwargs={
                'Room_Code': 'zH3l37Hn96ZkxyoMMc-V4w7xOchnerpDEfsjS7DsL1dAGGo',
                'Member_id': 5
            }),
            URL_Not_Found=reverse('Chat.api:Member', kwargs={
                'Room_Code': 'zH3l37Hn96ZkxyoMMc-V4w7xOchnerpDEfsjS7DsL1dAGGo',
                'Member_id': 4
            }),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    

    def test_not_admin(self):
        
        self._Authorize(os.environ.get('GUEST_USERNAME'), os.environ.get('GUEST_PASSWORD'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 403, self._Message('Not Admin'))

    
    def test_not_room_member(self):
        
        _response = requests.get(self._url_not_found, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Not Member'))


    def test_get_member(self):
        
        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Get Member'))

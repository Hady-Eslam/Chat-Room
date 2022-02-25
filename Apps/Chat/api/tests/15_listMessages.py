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
            API_Name='List Messages',
            URL=reverse('Chat.api:Messages', kwargs={
                'Room_Code': 'zH3l37Hn96ZkxyoMMc-V4w7xOchnerpDEfsjS7DsL1dAGGo',
            }),
            URL_Not_Found=reverse('Chat.api:Messages', kwargs={
                'Room_Code': 'zH3l37Hn96ZkxOchnerpDEfsjS7DsL1dAGGo',
            }),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    

    def test_not_room_member(self):

        self._Authorize(os.environ.get('GUEST_USERNAME'), os.environ.get('GUEST_PASSWORD'))
        
        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 403, self._Message('Not Member'))
    

    def test_list_messages_with_offset(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, params={
            'page_size': 5000,
            'page': 6
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('List Messages'))
    

    def test_list_messages(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('List Messages'))

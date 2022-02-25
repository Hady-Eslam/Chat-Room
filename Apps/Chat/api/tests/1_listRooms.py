from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import os, requests



class TestAPI(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PatchMethodNotAllowed
):
    def setUp(self):
        self._setUp(
            Production=False,
            API_Name='List Chat Rooms',
            URL=reverse('Chat.api:Rooms'),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    
    def test_list_chat_rooms_with_offset(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, params={
            'page_size': 5000,
            'page': 6
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('List Chat Rooms'))


    def test_list_chat_rooms(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('List Chat Rooms'))

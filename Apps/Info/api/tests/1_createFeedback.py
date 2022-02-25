from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os



class TestAPI(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.GetMethodNotAllowed, helper.PostInvalidData
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Feedback',
            URL=reverse('Info.api:Feedback'),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    
    def test_guest(self):

        self._Authorize(os.environ.get('GUEST_USERNAME'), os.environ.get('GUEST_PASSWORD'))

        _response = requests.post(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data={
            'title': 'Test API Feedback',
            'feedback': 'Test API Feedback',
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 403, self._Message('Guest User'))
    
    def test_create_feedback(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data={
            'title': 'Test API Feedback',
            'feedback': 'Test API Feedback',
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 201, self._Message('Create Feedback'))

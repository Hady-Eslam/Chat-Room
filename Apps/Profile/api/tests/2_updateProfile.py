from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, json, os



class TestApi(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PostMethodNotAllowed, 
):
    def setUp(self) -> None:
        self._setUp(
            Production=True,
            API_Name='Update Profile',
            URL=reverse('Profile.api:Profile'),
            Host=os.environ.get('HOST')
        )
        self._Authorize()
    

    def test_update_profile_without_data(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token),
        })

        self._print(_response)

        _Name = _response.json()['user']['first_name']
        _Bio = _response.json()['bio']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update User Profile Without Data'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['user']['first_name'] == _Name, self._Message('Update User Profile Without Data'))
        self.assertTrue(_response.json()['bio'] == _Bio, self._Message('Update User Profile Without Data'))
    

    def test_update_profile_with_name(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        _Name = _response.json()['user']['first_name']
        _Bio = _response.json()['bio']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data=json.dumps({
            'user': {'first_name': 'True Admin'}
        }))

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update User Profile With Name'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['user']['first_name'] != _Name, self._Message('Update User Profile Without Data'))
        self.assertTrue(_response.json()['bio'] == _Bio, self._Message('Update User Profile Without Data'))
    

    def test_update_profile_without_picture(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        _Name = _response.json()['user']['first_name']
        _Bio = _response.json()['bio']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data=json.dumps({
            'user': {'first_name': 'True Admin 2'},
            'bio': 'I Am The Admin 2'
        }))

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update User Profile With Name'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['user']['first_name'] != _Name, self._Message('Update User Profile Without Data'))
        self.assertTrue(_response.json()['bio'] != _Bio, self._Message('Update User Profile Without Data'))
    

    def test_update_profile_with_readonly_data(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        _Name = _response.json()['user']['first_name']
        _Is_Active = _response.json()['user']['is_active']
        _Created_At = _response.json()['created_at']
        _Bio = _response.json()['bio']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data=json.dumps({
            'user': {'first_name': 'True Admin 4', 'is_active': False},
            'bio': 'I Am The Admin 4',
            'created_at': '2022-02-08 17:30:26.750078'
        }))

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update User Profile With Name'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['user']['first_name'] != _Name, self._Message('Update User Profile Without Data'))
        self.assertTrue(_response.json()['user']['is_active'] == _Is_Active, self._Message('Update User Profile Without Data'))
        self.assertTrue(_response.json()['created_at'] == _Created_At, self._Message('Update User Profile Without Data'))
        self.assertTrue(_response.json()['bio'] != _Bio, self._Message('Update User Profile Without Data'))

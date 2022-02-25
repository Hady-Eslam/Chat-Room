from django.test import SimpleTestCase
from django.urls import reverse
from ... import helper
import requests, os, json



class TestAPI(
    SimpleTestCase, helper.TestAPIHelper, helper.NoVersion, helper.InvalidVersion, helper.NotAuthenticated,
    helper.PostMethodNotAllowed, helper.PatchRoomNotFound
):
    def setUp(self) -> None:
        self._setUp(
            Production=False,
            API_Name='Change Room Settings',
            URL=reverse('Chat.api:Settings', kwargs={
                'Room_Code': 'zH3l37Hn96ZkxyoMMc-V4w7xOchnerpDEfsjS7DsL1dAGGo'
            }),
            URL_Not_Found=reverse('Chat.api:Settings', kwargs={
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
    

    def test_update_room_settings_without_data(self):

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token),
        })

        self._print(_response)

        _Name = _response.json()['name']
        _Description = _response.json()['description']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update Room Settings Without Data'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['name'] == _Name, self._Message('Update oom Settings Without Data'))
        self.assertTrue(_response.json()['description'] == _Description, self._Message('Update oom Settings Without Data'))
    

    def test_update_room_settings_with_name(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        _Name = _response.json()['name']
        _Description = _response.json()['description']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data=json.dumps({
            'name': 'Edited Test API Name'
        }))

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update Room Settings With Name'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['name'] != _Name, self._Message('Update Room Settings Without Data'))
        self.assertTrue(_response.json()['description'] == _Description, self._Message('Update Room Settings Without Data'))
    

    def test_update_profile_without_cover(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        _Name = _response.json()['name']
        _Description = _response.json()['description']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data=json.dumps({
            'name': 'Edited Test API Name 2',
            'description': 'Edited Description 2'
        }))

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update Room Settings With Name'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['name'] != _Name, self._Message('Update Room Settings Without Data'))
        self.assertTrue(_response.json()['description'] != _Description, self._Message('Update Room Settings Without Data'))
    

    def test_update_profile_with_readonly_data(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        _Name = _response.json()['name']
        _Description = _response.json()['description']
        _Created_At = _response.json()['created_at']
        _Code = _response.json()['code']

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self._Token)
        }, data=json.dumps({
            'name': 'Edited Test API Name 3',
            'description': 'Edited Description 3',
            'code': 'fdsfdsfdsf',
            'created_at': '2022-02-08 17:30:26.750078'
        }))

        self._print(_response)

        self.assertTrue(_response.status_code == 200, self._Message('Update Room Settings With Name'))

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.json()['name'] != _Name, self._Message('Update Room Settings Without Data'))
        self.assertTrue(_response.json()['description'] != _Description, self._Message('Update Room Settings Without Data'))
        self.assertTrue(_response.json()['created_at'] == _Created_At, self._Message('Update Room Settings Without Data'))
        self.assertTrue(_response.json()['code'] == _Code, self._Message('Update Room Settings Without Data'))

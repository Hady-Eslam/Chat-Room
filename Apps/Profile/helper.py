from django.urls import reverse
import requests, json, secrets, random, os



class Random:

    @classmethod
    def create_random_token(cls, _Min_Length=50, _Length=50):
        return ''.join(secrets.token_urlsafe(random.randrange(_Min_Length, _Length)))
        
        # Old Solution
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits + string.ascii_lowercase
            ) for _ in range(
            random.randrange(_Min_Length, _Length)
        ))



class TestAPIHelper:

    _url = ''
    _url_not_found = ''
    __Token_Url = ''
    __API_Name = ''


    def _setUp(self, Production=False, API_Name='', URL='', URL_Not_Found='', Host='') -> None:

        _Host = Host if Production else 'http://127.0.0.1:8000'
        
        self._url = _Host + URL
        self._url_not_found = _Host + URL_Not_Found
        self.__Token_Url = _Host + reverse('Auth.api:Token')
        self.__API_Name = API_Name


    def _print(self, _response):
        try:
            print('\n', _response.url, '\t', _response.status_code, '\t', json.dumps(
                    _response.json(), indent=4, sort_keys=True), end='\n\n')
        except Exception as e:
            print('\n', _response.url, '\t', _response.status_code, '\t', _response.content, end='\n\n')


    def _Authorize(self, username=None, password=None):
        self._Token = None
        self._Refresh = None

        _response = requests.post(self.__Token_Url, data={
            'username': username if username else os.environ.get('SUPER_USER_USERNAME'),
            'password': password if password else os.environ.get('SUPER_USER_PASSWORD')
        })

        self._Token = _response.json()['access']
        self._Refresh = _response.json()['refresh']


    def _Message(self, Message):
        return '{0} Testing Api: ( {1} )'.format(self.__API_Name, Message)





class NoVersion:

    def test_no_version(self):

        _response = requests.get(self._url)
        
        self._print(_response)
        
        self.assertTrue(_response.status_code == 426, self._Message('No Version'))


class InvalidVersion:

    def test_invalid_version(self):

        _response = requests.get(self._url, headers={
            'Version': 'V5'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 426, self._Message('Invalid Version'))


class GetMethodNotAllowed:

    def test_get_method_not_allowed(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 405, self._Message('Get_Method Not Allowed'))


class PostMethodNotAllowed:

    def test_post_method_not_allowed(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 405, self._Message('Post Method Not Allowed'))


class PatchMethodNotAllowed:

    def test_patch_method_not_allowed(self):

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 405, self._Message('Patch Method Not Allowed'))


class PostInvalidData:

    def test_post_invalid_data(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 400, self._Message('Invalid Post Data'))


class PatchInvalidData:

    def test_patch_invalid_data(self):

        _response = requests.patch(self._url, headers={
            'Version': 'V1',
            'Authorization': 'Bearer {0}'.format(self._Token)
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 400, self._Message('Invalid Patch Data'))


class TokenNotInQuery:

    def test_token_not_in_query(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Token Not in Query'))


class TokenNotFound:

    def test_token_not_found(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1'
        }, params={
            'Token': 'sfsdfdsfdsfdsfdsfds'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Token Not Found'))


class NotAuthenticated:

    def test_not_authenticated(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 401, self._Message('Not Authenticated'))

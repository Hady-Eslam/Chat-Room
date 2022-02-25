import random, string, requests, json, secrets
from rest_framework.request import Request
from rest_framework.reverse import reverse as api_reverse
from django.urls import reverse
from django.http import HttpRequest
from .models import UserToken
import os


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




class MessageStorage:

    SESSION_KEY_NAME = 'MESSAGE_STORAGE_KEY'

    def __init__(self, request: HttpRequest) -> None:
        self.__request = request
        self.__Exists_Op = False
        if self.SESSION_KEY_NAME not in self.__request.session:
            self.__request.session[self.SESSION_KEY_NAME] = {}

    def __getattr__(self, attr):
        if self.__Exists_Op:
            self.__Exists_Op = False
            return attr in self.__request.session[self.SESSION_KEY_NAME]
        
        try:
            _value = self.__request.session[self.SESSION_KEY_NAME].pop(attr)
            self.__request.session.modified = True

            return _value
        except Exception:
            return None
    

    def set(self, __name, __value):
        self.__request.session[self.SESSION_KEY_NAME][__name] = __value
        self.__request.session.modified = True
    

    def exists(self):
        self.__Exists_Op = True
        return self





class Email:

    @classmethod
    def __Send_Confirm(cls, _Token: UserToken, _Link):
        _Token.user.email_user(
            subject='Confirm Signup Process',
            message='Please Click On This Email To Confirm The Signup < {0} >'.format(_Link),
            html_message="""
                Please Click On This Link To Complete The Signup Process <a href="{0}">Click Here</a>
            """.format(_Link)
        )
    

    @classmethod
    def __SendResetPassword(cls, _Token: UserToken, _Link):
        _Token.user.email_user(
            subject='Reset Password Process',
            message='Please Click On This Email To Reset Your Password < {0} >'.format(_Link),
            html_message="""
                Please Click On This Link To Reset Your Password <a href="{0}">Click Here</a>
            """.format(_Link)
        )


    @classmethod
    def sendConfirm(cls, _Token: UserToken, _build_absolute_uri):
        cls.__Send_Confirm(_Token, _build_absolute_uri(
            reverse('Auth:Confirm-Signup') + '?Token=' + _Token.token
        ))
    

    @classmethod
    def SendResetPassword(cls, _Token: UserToken, _build_absolute_uri):
        cls.__SendResetPassword(_Token, _build_absolute_uri(
            reverse('Auth:Reset-Password') + '?Token=' + _Token.token
        ))
    

    @classmethod
    def apiSendConfirm(cls, request: Request, _Token: UserToken):
        cls.__Send_Confirm(_Token,
            api_reverse('Auth.api:Confirm-Signup', request=request) + '?Token=' + _Token.token
        )
    

    @classmethod
    def apiSendResetPassword(cls, request: Request, _Token: UserToken):
        cls.__SendResetPassword(_Token,
            api_reverse('Auth.api:Reset-Password', request=request) + '?Token=' + _Token.token
        )



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
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 405, self._Message('Get_Method Not Allowed'))


class PostMethodNotAllowed:

    def test_post_method_not_allowed(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 405, self._Message('Post Method Not Allowed'))


class PatchMethodNotAllowed:

    def test_patch_method_not_allowed(self):

        _response = requests.patch(self._url, headers={
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 405, self._Message('Patch Method Not Allowed'))


class PostInvalidData:

    def test_post_invalid_data(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 400, self._Message('Invalid Post Data'))


class TokenNotInQuery:

    def test_token_not_in_query(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Token Not in Query'))


class PostTokenNotInQuery:

    def test_token_not_in_query(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Post Token Not in Query'))


class TokenNotFound:

    def test_token_not_found(self):

        _response = requests.get(self._url, headers={
            'Version': 'V1'
        }, params={
            'Token': 'sfsdfdsfdsfdsfdsfds'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Token Not Found'))


class PostTokenNotFound:

    def test_token_not_found(self):

        _response = requests.post(self._url, headers={
            'Version': 'V1'
        }, params={
            'Token': 'sfsdfdsfdsfdsfdsfds'
        })

        self._print(_response)

        self.assertTrue(_response.status_code == 404, self._Message('Post Token Not Found'))

from rest_framework import exceptions
from rest_framework import status
from rest_framework.versioning import BaseVersioning


class VersionException(exceptions.APIException):
    status_code = status.HTTP_426_UPGRADE_REQUIRED
    default_detail = 'invalid version'
    default_code = 'invalid version'

class Versioning(BaseVersioning):

    default_version = None
    allowed_versions = ['V1']

    invalid_version_message = 'Invalid Version'

    def determine_version(self, request, *args, **kwargs):
        _Version = request.META.get('HTTP_VERSION')
        if not self.is_allowed_version(_Version):
            raise VersionException(self.invalid_version_message)
        return _Version

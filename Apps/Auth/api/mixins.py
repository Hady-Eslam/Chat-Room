from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from .throttles import AuthThrottleClass
from .versioning import Versioning


class BaseMixin:
    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottleClass]
    renderer_classes = [JSONRenderer]
    versioning_class = Versioning

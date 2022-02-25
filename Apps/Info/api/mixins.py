from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from .throttles import InfoThrottleClass
from .versioning import Versioning


class BaseMixin:
    permission_classes = [IsAuthenticated]
    throttle_classes = [InfoThrottleClass]
    renderer_classes = [JSONRenderer]
    versioning_class = Versioning

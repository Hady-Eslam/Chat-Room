from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from ..models import Profile
from .versioning import Versioning
from .throttles import ProfileThrottleClass


class BaseProfileAPI:
    permission_classes = [IsAuthenticated]
    throttle_classes = [ProfileThrottleClass]
    renderer_classes = [JSONRenderer]
    versioning_class = Versioning


class ProfileAPIMixin:

    def initial(self, request, *args, **kwargs):
        super(ProfileAPIMixin, self).initial(request, *args, **kwargs)

        if request.user.is_authenticated:
            self.profile = Profile.objects.filter(user=request.user).first()
            if self.profile is None:
                self.profile = Profile()
                self.profile.user = request.user
                self.profile.save()
        else:
            self.profile = None

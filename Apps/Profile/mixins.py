from .models import Profile

class ProfileMixin:

    profile = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.profile = Profile.objects.filter(user=request.user).first()
            if self.profile is None:
                self.profile = Profile()
                self.profile.user = request.user
                self.profile.save()
        else:
            self.profile = None
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(profile=self.profile, **kwargs)

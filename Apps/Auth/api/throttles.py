from rest_framework.throttling import ScopedRateThrottle

class AuthThrottleClass(ScopedRateThrottle):

    def allow_request(self, request, view):
        scope = getattr(view, self.scope_attr, None)
        if scope and len(scope) > 1:
            self.THROTTLE_RATES[scope[0]] = scope[1]
            setattr(view, self.scope_attr, scope[0])
        return super().allow_request(request, view)

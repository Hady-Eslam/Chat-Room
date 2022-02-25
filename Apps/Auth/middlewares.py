from django.utils.deprecation import MiddlewareMixin
from .helper import MessageStorage



class FlashMessage(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response
    

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        request.flash_message = MessageStorage(request)

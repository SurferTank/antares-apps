from threading import current_thread
from django.utils.deprecation import MiddlewareMixin

_requests = {}


def get_request():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t]


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _requests[current_thread()] = request

from threading import current_thread
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

_requests = {}


def get_request():
    """this includes a dirty hack for testing  """
    from django.conf import settings
    from django.test.client import RequestFactory
    from antares.apps.user.models.user import User
    try:
        settings.TEST_MODE
    except:
        settings.TEST_MODE = False
    if settings.TEST_MODE == True:
        request_factory = RequestFactory()
        request = request_factory.post("/")
        request.user = User.get_test_user()
        request.session = {}
        return request
    else:
        t = current_thread()
        if t not in _requests:
            return None
        return _requests[t]


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _requests[current_thread()] = request

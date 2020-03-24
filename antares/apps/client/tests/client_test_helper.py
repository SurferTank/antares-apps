'''
Created on Nov 6, 2017

@author: leobelen
'''
from antares.apps.client.constants import ClientArchetype
from antares.apps.client.models import Client, ClientType
from antares.apps.core.middleware import get_request
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class ClientTestHelper:

    def create_test_user_client(self):
        client_type = ClientType()
        client_type.archetype = ClientArchetype.INDIVIDUAL
        client_type.id = 'INDIVIDUAL'
        client_type.save()

        client = Client()
        client.client_type = client_type
        client.code = "12345"
        client.user = get_request().user
        client.first_name = "test"
        client.last_name = "user"
        client.registration_date = datetime.now().date()
        client.save()
        get_request().user.refresh_from_db()
        return client

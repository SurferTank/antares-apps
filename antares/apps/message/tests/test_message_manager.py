'''
Created on Nov 5, 2017

@author: leobelen
'''
import logging
import os
from datetime import datetime

from django.test import TransactionTestCase 
from ..service import MessageManager
from antares.apps.document.constants import DocumentStatusType, FormClassType, FormClassStatusType, FormDefinitionStatusType
from antares.apps.document.models import FormClass, FormDefinition
from antares.apps.client.models import Client, ClientType
from antares.apps.client.constants import ClientArchetype
from antares.apps.user.models import User
from antares.apps.core.middleware import get_request

logger = logging.getLogger(__name__)

class TestMessageManager(TransactionTestCase):
    multi_db = True
    runs = 0
    message = """
    {
        "documents": [
            {
                "type": "account_form", 
                    "post_date": "2001-01-01T00:00:00+3",
                 "create_summary": false,
                "header": [
                    {
                        "period": 2001
                    }
                ],
            "fields": [
                {
                    "someVariableOnMessage": 100.1
                }
            ]
            }
        ]
    }
    """
    
    def setUp(self):
        TransactionTestCase.setUp(self)
        if self.runs == 0:
            with open(os.path.join(os.path.dirname(__file__), "..", "..", "document", "xml", "working", "AccountForm-1.xml"), "r") as xml:
                self.form_xml = xml.read()
            self.runs = self.runs + 1
    
    def create_form_class(self):
        logger.info("we are testing if we can create a form class")
        form_class = FormClass()
        form_class.name = "testForm"
        form_class.description = "some description"
        form_class.type = FormClassType.ADMINISTRATIVE
        form_class.status = FormClassStatusType.DEVELOPMENT
        form_class.author = User.get_test_user()
        form_class.third_party_type = "account_form"
        form_class.save()
        logger.info("form class with name" + form_class.name + " created")
        return form_class
    
    def create_form_definition(self):
        form_class = self.create_form_class()
        form_def = FormDefinition()
        form_def.definition = self.form_xml
        form_def.status = FormDefinitionStatusType.DEVELOPMENT
        form_def.form_class = form_class
        form_def.start_date = datetime.now()
        form_def.author = User.get_test_user()
        form_def.process_form_definition_loading()
        form_def.save()
        logger.info("form definition with id " + form_def.id + " created")
        return form_def
    
    def setup_testuser_client(self):
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
    
    def test_form_definition_creation(self):
        self.create_form_definition()
    
    def test_document_creation(self):
        self.setup_testuser_client()
        self.create_form_definition()
        MessageManager.create_docs_from_message(self.message)
        
        
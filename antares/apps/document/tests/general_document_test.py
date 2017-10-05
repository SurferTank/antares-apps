import logging
import os

from django.test import TestCase
from ..models import FormDefinition, FormClass
from ..constants import FormClassType, FormClassStatusType, FormDefinitionStatusType
from antares.apps.user.models import User
from datetime import datetime

logger = logging.getLogger(__name__)

class GeneralDocumentTest(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        self.test_user = User.get_test_user()
        with open(os.path.join(os.path.dirname(__file__), "..", "xml", "working", "AccountForm-1.xml"), "r") as xml:
            self.form_xml = xml.readlines()
        #self.user = User.get_system_user()
    
    def test_admin_form_class_creation(self):
        logger.info("we are testing if we can create a form class")
        form_class = FormClass()
        form_class.name = "testForm"
        form_class.description = "some description"
        form_class.type = FormClassType.ADMINISTRATIVE
        form_class.status = FormClassStatusType.DEVELOPMENT
        form_class.author = self.test_user
        form_class.save()

        logger.info("form class created with name " + str(form_class.name))
        return form_class
    
    def test_form_creation(self):
        logger.info("we are testing if we can create a form class")
        form_def = FormDefinition()
        form_def.definition = self.form_xml
        form_def.status = FormDefinitionStatusType.DEVELOPMENT
        form_def.start_date = datetime.now()
        form_def.author = self.test_user
        FormDefinition.process_form_definition_loading(form_def)
        form_def.save()
    
    def test_document_creation(self):
        logger.info("we are testing if a document can be created")
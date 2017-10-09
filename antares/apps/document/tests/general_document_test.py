import logging
import os

from django.test import TransactionTestCase 
from ..models import FormDefinition, FormClass
from ..constants import FormClassType, FormClassStatusType, FormDefinitionStatusType
from antares.apps.user.models import User
from datetime import datetime

logger = logging.getLogger(__name__)

class GeneralDocumentTest(TransactionTestCase):
    multi_db = True
    runs = 0
    def setUp(self):
        TransactionTestCase.setUp(self)
        if self.runs == 0:
            with open(os.path.join(os.path.dirname(__file__), "..", "xml", "working", "AccountForm-1.xml"), "r") as xml:
                self.form_xml = xml.readlines()
            self.runs = self.runs + 1
    
    def test_form_definition_creation(self):
        logger.info("we are testing if we can create a form class")
        form_class = FormClass()
        form_class.name = "testForm"
        form_class.description = "some description"
        form_class.type = FormClassType.ADMINISTRATIVE
        form_class.status = FormClassStatusType.DEVELOPMENT
        form_class.author = User.get_test_user()
        form_class.save()
        logger.info("form class with name" + form_class.name + " created")
    
        form_def = FormDefinition()
        form_def.definition = self.form_xml
        form_def.status = FormDefinitionStatusType.DEVELOPMENT
        form_def.form_class = form_class
        form_def.start_date = datetime.now()
        form_def.author = User.get_test_user()
        #FormDefinition.process_form_definition_loading(form_def)
        form_def.save()
        logger.info("form definition with id " + form_def.id + " created")
        
    
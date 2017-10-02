import logging

from django.test import TestCase
from ..models import FormDefinition, FormClass
from ..constants import FormClassType, FormClassStatusType
from antares.apps.user.models import User

logger = logging.getLogger(__name__)

class GeneralDocumentTest(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        self.test_user = User.get_test_user()
        #self.user = User.get_system_user()
    
    def test_admin_form_class_creation(self):
        logger.info("we are testing if we can create a form class")
        form_class = FormClass()
        form_class.name = "test form"
        form_class.description = "some description"
        form_class.type = FormClassType.ADMINISTRATIVE
        form_class.status = FormClassStatusType.DEVELOPMENT
        form_class.author = self.test_user
        form_class.save()

        logger.info("form class created with id " + str(form_class.id))
        return form_class
    
    def test_form_creation(self):
        
        form_def = FormDefinition()
        
    
    def test_document_creation(self):
        logger.info("we are testing if a document can be created")
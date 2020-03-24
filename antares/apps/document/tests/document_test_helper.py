'''
Created on Nov 6, 2017

@author: leobelen
'''
from antares.apps.client.tests.client_test_helper import ClientTestHelper
from antares.apps.user.models import User
from datetime import datetime
import logging
import os

from ..constants import FormClassType, FormClassStatusType, FormDefinitionStatusType
from ..models import FormDefinition, FormClass


logger = logging.getLogger(__name__)


class DocumentTestHelper(object):
    '''
    Defines functions to help on the document tests, so we don't 
    have to write the same stuff over and over again. 
    '''

    def get_test_form_id(self):
        return "AccountForm-1"

    def __init__(self):
        xmlFile = os.path.join(
                    os.path.dirname(__file__),
                    self.get_test_form_id() + ".xml")
        with open(xmlFile, "r") as xml:
            self.form_xml = str(xml.read())
        self.client_helper = ClientTestHelper()

    def create_test_form_class(self):
        logger.info("we are testing if we can create a form class")
        self.client_helper.create_test_user_client()
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

    def create_test_form_definition(self):
        form_class = self.create_test_form_class()
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
   

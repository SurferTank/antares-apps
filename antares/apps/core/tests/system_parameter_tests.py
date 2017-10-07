'''
Created on Oct 6, 2017

@author: leobelen
'''
import logging
import os

from django.test import TransactionTestCase 
from ..models import SystemParameter
from ..constants import FieldDataType
from antares.apps.core.middleware import RequestMiddleware 


logger = logging.getLogger(__name__)

class SystemParameterTest(TransactionTestCase):
    multi_db = True
    def setUp(self):
        TransactionTestCase.setUp(self)
            
    def test_string_param(self):
        param_text = SystemParameter.find_one("STRING_PARAM", FieldDataType.STRING, "test", "some test")
        self.assertEqual(param_text, "test")
        param_text = SystemParameter.find_one("STRING_PARAM", FieldDataType.STRING, "another_test")
        self.assertEqual(param_text, "test")
        logger.info("we could create a string sysparam with value " + param_text)
    def test_text_param(self):
        param_text = SystemParameter.find_one("TEXT_PARAM", FieldDataType.TEXT, "test", "some test")
        self.assertEqual(param_text, "test")
        param_text = SystemParameter.find_one("TEXT_PARAM", FieldDataType.TEXT, "another_test")
        self.assertEqual(param_text, "test")
        logger.info("we could create a text sysparam with value " + param_text)
        
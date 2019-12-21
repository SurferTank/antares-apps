'''
Created on Oct 6, 2017

@author: leobelen
'''
import logging
import datetime
from uuid import uuid4

from django.test import TransactionTestCase
from ..models import UserParameter
from ..enums import FieldDataType

logger = logging.getLogger(__name__)


class UserParameterTest(TransactionTestCase):
    """ Tests the User Parameter Model """

    def setUp(self):
        TransactionTestCase.setUp(self)

    def test_string_param(self):
        param_value = UserParameter.find_one(
            "STRING_PARAM", FieldDataType.STRING, "test", "some test")
        self.assertEqual(param_value, "test")
        param_value = UserParameter.find_one(
            "STRING_PARAM", FieldDataType.STRING, "another_test")
        self.assertEqual(param_value, "test")
        logger.info("we could create a string sysparam with value " +
                    param_value)

    def test_text_param(self):
        param_value = UserParameter.find_one("TEXT_PARAM", FieldDataType.TEXT,
                                             "test", "some test")
        self.assertEqual(param_value, "test")
        param_value = UserParameter.find_one("TEXT_PARAM", FieldDataType.TEXT,
                                             "another_test")
        self.assertEqual(param_value, "test")
        logger.info("we could create a text sysparam with value " +
                    param_value)

    def test_integer_param(self):
        param_value = UserParameter.find_one(
            "INTEGER_PARAM", FieldDataType.INTEGER, 1, "some test")
        self.assertEqual(param_value, 1)
        param_value = UserParameter.find_one("INTEGER_PARAM",
                                             FieldDataType.INTEGER, 2)
        self.assertEqual(param_value, 1)
        logger.info("we could create a integer sysparam with value " +
                    str(param_value))

    def test_float_param(self):
        param_value = UserParameter.find_one(
            "FLOAT_PARAM", FieldDataType.FLOAT, 1.1, "some test")
        self.assertEqual(param_value, 1.1)
        param_value = UserParameter.find_one("FLOAT_PARAM",
                                             FieldDataType.FLOAT, 2.0)
        self.assertEqual(param_value, 1.1)
        logger.info("we could create a float sysparam with value " +
                    str(param_value))

    def test_date_param(self):
        param_value = UserParameter.find_one("DATE_PARAM", FieldDataType.DATE,
                                             datetime.date(2001, 1, 1),
                                             "some test")
        self.assertEqual(param_value, datetime.date(2001, 1, 1))
        param_value = UserParameter.find_one("DATE_PARAM", FieldDataType.DATE,
                                             datetime.date(2011, 1, 1))
        self.assertEqual(param_value, datetime.date(2001, 1, 1))
        logger.info("we could create a float sysparam with value " +
                    str(param_value))

    def test_datetime_param(self):
        param_value = UserParameter.find_one(
            "DATETIME_PARAM", FieldDataType.DATETIME,
            datetime.datetime(2001, 1, 1, 1, 1, 1), "some test")
        self.assertEqual(param_value, datetime.datetime(2001, 1, 1, 1, 1, 1))
        param_value = UserParameter.find_one(
            "DATETIME_PARAM", FieldDataType.DATETIME,
            datetime.datetime(2011, 1, 1, 1, 1, 1))
        self.assertEqual(param_value, datetime.datetime(2001, 1, 1, 1, 1, 1))
        logger.info("we could create a float sysparam with value " +
                    str(param_value))

    def test_uuid_param(self):
        uuid_1 = uuid4()
        uuid_2 = uuid4()
        param_value = UserParameter.find_one("UUID_PARAM", FieldDataType.UUID,
                                             uuid_1, "some test")
        self.assertEqual(param_value, uuid_1)
        param_value = UserParameter.find_one("UUID_PARAM", FieldDataType.UUID,
                                             uuid_2, "some test")
        self.assertEqual(param_value, uuid_1)
        logger.info("we could create a float sysparam with value " +
                    str(param_value))

    #def test_bool_param(self):
    #    param_value = UserParameter.find_one("BOOL_PARAM", FieldDataType.BOOLEAN, True, "some test")
    #    self.assertEqual(param_value, True)
    #    param_value = UserParameter.find_one("UUID_PARAM", FieldDataType.BOOLEAN, False, "some test")
    #    self.assertEqual(param_value,  True)
    #    logger.info("we could create a float sysparam with value " + str(param_value))

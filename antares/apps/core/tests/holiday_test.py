from django.test import TransactionTestCase 

class HolidayTest(TransactionTestCase):
    """ Test the infrastructure to handle Holidays """
    
    def setUp(self):
        TransactionTestCase.setUp(self)
    
    def test_holiday(self):
        self.assertFalse(False)
from django.test import TransactionTestCase 
from datetime import date
from ..models import Holiday

class HolidayTest(TransactionTestCase):
    """ Test the infrastructure to handle Holidays """
    
    def setUp(self):
        TransactionTestCase.setUp(self)
    
    def test_holiday_next_on_saturday(self):
        saturday = date(2017, 9, 9)
        next_day = Holiday.next_day(saturday)
        self.assertEqual(next_day, date(2017, 9, 11))
    
    def test_holiday_prev_on_monday(self):
        monday = date(2017, 9, 11)
        prev_day = Holiday.prev_day(monday)
        self.assertEqual(prev_day, date(2017, 9, 8))
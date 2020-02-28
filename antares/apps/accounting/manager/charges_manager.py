""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""

import logging
from django.utils import timezone
logger = logging.getLogger(__name__)
from ..models import InterestDefinition
from ..models import PenaltyDefinition
from antares.apps.core.manager import PeriodManager
from antares.apps.obligation.models import ObligationVector
from ..models import AccountCharge

class ChargesManager(object):
    should_calculate = False
    
    def __init__(self, account_balance, current_date=timezone.now()):
        self.account_balance = account_balance
        self.current_date = current_date
        
        self.obligation = ObligationVector.find_one_by_COPAD(account_balance.get_COPAD())
        self.interest_def_list = InterestDefinition.findAllAndByConceptType(self.account_balance.concept_type)
        self.penalties_def_list = PenaltyDefinition.findAllAndByConceptType(self.account_balance.concept_type)
        
        if (self.obligation is not None and 
           self.account_balance.principal_balance > 0):
            self.should_calculate = True 
    
    def calculateCharges(self, event_date = timezone.now(), invalidateCharges=False):
        if(not self.should_calculate or self.account_balance.compliance_date is None):
            return 
        self.processInterest(invalidateCharges)
        self.processPenalties(invalidateCharges) 
        
    
    def processInterest(self, event_date, invalidateCharges):
        logger.info("Processing interest")
        for interestDef in self.interest_def_list:
            periodList = PeriodManager.find_period_list_by_client_obligation(self.obligation.client_obligation, event_date)
            return
        
            
    def processPenalties(self, event_date, invalidateCharges):
        logger.info("Processing interest")
        for penaltyDef in self.penalties_def_list:
            return
        
        
    
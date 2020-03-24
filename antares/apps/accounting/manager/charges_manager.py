""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""

from antares.apps.core.manager import PeriodManager
from antares.apps.document.constants import DocumentStatusType
from antares.apps.document.types import Document
from antares.apps.obligation.models import ObligationVector
import logging

from django.utils import timezone

from ..models import AccountBalance
from ..models import AccountCharge
from ..models import InterestDefinition
from ..models import PenaltyDefinition


logger = logging.getLogger(__name__)


class ChargesManager(object):
    
    def calculateChargesByClient(self, client):
        
        balanceList = AccountBalance.findByClient(client)
        for balance in balanceList:
            self.calculateChargesByAccount(balance)
    
    def calculateChargesByAccount(self, account_balance, event_date=timezone.now(),
                                  invalidate_charges=False):
        
        obligation = ObligationVector.find_one_by_COPAD(account_balance.get_COPAD())
        interest_def_list = InterestDefinition.findAllAndByConceptType(account_balance.concept_type)
        penalty_def_list = PenaltyDefinition.findAllAndByConceptType(account_balance.concept_type)
        
        if (obligation is not None
             and  account_balance.principal_balance.amount < 0):
            should_calculate = True 
        else:
            should_calculate = False
        if(not should_calculate):
            return 
        self.processInterest(event_date, account_balance, obligation,
                             interest_def_list, should_calculate, invalidate_charges)
        self.processPenalties(event_date, account_balance, obligation,
                              penalty_def_list, should_calculate, invalidate_charges) 
    
    def processInterest(self, event_date, account_balance, obligation, interest_def_list,
                        should_calculate, invalidate_charges):
        logger.info("Processing interest")
        for interestDef in interest_def_list:
            periodList = PeriodManager.find_period_list_by_client_obligation(obligation.client_obligation,
                                                                             event_date)
            for period in periodList:
                interestRecord = AccountCharge.findByCOPADChargePeriodAndInterestDefinition(account_balance.get_COPAD(),
                                                                                             period, interestDef)
                if(interestRecord is None or invalidate_charges):
                    self.calculateInterest(event_date, account_balance, obligation,
                                           should_calculate, invalidate_charges, interestDef,
                                           period, interestRecord)
            
    def calculateInterest(self, event_date, account_balance, obligation, should_calculate,
                          invalidate_charges, definition, period, record):
        if(record is None):
            record = AccountCharge()
            record.setCOPADPeriodInterestDefinition(account_balance.get_COPAD(), period, definition)
        record.amount = account_balance.principal_balance * definition.rate
        interestDoc = Document(formId="Interest-1")
        interestDoc.set_COPAD(account_balance.get_COPAD())
        interestDoc.set_field_value("aPeriod", 200101)
        interestDoc.set_field_value("aAmount", record.amount)        
        interestDoc.save(DocumentStatusType.SAVED)
        record.charge_document = interestDoc
        record.save()
            
    def processPenalties(self, event_date, account_balance, obligation,
                              penalty_def_list, should_calculate, invalidate_charges):
        logger.info("Processing interest")
        for penaltyDef in penalty_def_list:
            logger.info("Processing interest")
            penaltyRecord = AccountCharge.findByCOPADChargePeriodAndInterestDefinition(account_balance.get_COPAD(),
                                                                                             0, penaltyDef)
            if(penaltyRecord is None or invalidate_charges):
                self.calculatePenalties(event_date, account_balance, obligation,
                                           should_calculate, invalidate_charges, 0, penaltyDef, penaltyRecord)
        
    def calculatePenalties(self, event_date, account_balance, obligation,
                                           should_calculate, invalidate_charges,
                                           period, definition, record):
        if(record is None):
            record = AccountCharge()
            record.setCOPADPeriodPenaltyDefinition(account_balance.get_COPAD(), period, definition)
        record.amount = account_balance.principal_balance
        if(definition.rate is not None and definition.rate > 0):
            record.amount = record.amount * definition.rate
        if(definition.fixed_amount is not None and definition.fixed_amount > 0):
            record.amount = record.amount + definition.fixed_amount
        penaltyDoc = Document(formId="Penalty-1")
        penaltyDoc.set_COPAD(account_balance.get_COPAD())
        penaltyDoc.set_field_value("aPeriod", 200101)
        penaltyDoc.set_field_value("aAmount", record.amount)        
        penaltyDoc.save(DocumentStatusType.SAVED)
        record.charge_document = penaltyDoc
        record.save()

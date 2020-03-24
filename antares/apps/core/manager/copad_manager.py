'''
Created on Feb 19, 2020

@author: leobelen
'''


class COPAD(object):
    """ A simple class to move around the account headers """

    def __init__(self, client=None, concept_type=None, period=None, account_type=None, document=None):
        self.client = client
        self.concept_type = concept_type
        self.period = period
        self.account_type = account_type
        self.document = document 
        
    def __eq__(self, rVal):
        if not isinstance(rVal, COPAD):
            raise RuntimeError("COPAD can be only compared to another COPAD")
        if(self.client == rVal.client and 
           self.concept_type == rVal.concept_type and 
           self.period == rVal.period and 
           self.account_type == rVal.account_type and 
           self.document == rVal.document):
            return True
        return False

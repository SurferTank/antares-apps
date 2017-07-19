""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""

class NegativeAmountException(Exception):
    """ Indicates an unauthorized negative amount was entered into the current account. 
    """
    
    def __init__(self, value):
        """ Initial value settings 
        """
        self.value = value

    def __str__(self):
        """ Gets a string representation of the exception 
        """
        return repr(self.value)

""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""

class MissingAccountHeaderInformationException(Exception):
    """ Indicates a problem exists with the header information of the current account. 
    """

    def __init__(self, value):
        """ Initial value settings 
        """
        self.value = value

    def __str__(self):
        """ Gets a string representation of the exception 
        """
        return repr(self.value)

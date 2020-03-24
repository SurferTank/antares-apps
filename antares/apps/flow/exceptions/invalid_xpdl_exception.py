'''
Created on Jul 5, 2016

@author: leobelen
'''


class InvalidXPDLException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

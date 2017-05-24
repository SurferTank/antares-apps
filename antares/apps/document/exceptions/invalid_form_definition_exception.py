'''
Created on Jun 14, 2016

@author: leobelen
'''


class InvalidFormDefinitionException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

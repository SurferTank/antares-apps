'''
Created on Jun 23, 2016

@author: leobelen
'''


class NegativeAmountException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

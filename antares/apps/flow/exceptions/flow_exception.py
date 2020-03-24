'''
Created on Jul 12, 2016

@author: leobelen
'''


class FlowException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

'''
Created on Jul 16, 2016

@author: leobelen
'''


class InvalidStatusException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

'''
Created on Jul 18, 2016

@author: leobelen
'''


class UserException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

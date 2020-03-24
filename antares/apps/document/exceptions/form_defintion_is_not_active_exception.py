'''
Created on Jun 15, 2016

@author: leobelen
'''


class FormDefintionIsNotActiveException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

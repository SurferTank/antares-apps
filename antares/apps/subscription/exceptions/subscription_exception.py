'''
Created on Jul 9, 2016

@author: leobelen
'''


class SubscriptionException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

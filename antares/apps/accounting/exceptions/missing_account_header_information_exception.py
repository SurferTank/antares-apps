'''
Created on Jun 22, 2016

@author: leobelen
'''


class MissingAccountHeaderInformationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

'''
Created on Jun 26, 2016

@author: leobelen
'''


class InvalidDocumentValueException(Exception):
    '''
    classdocs
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

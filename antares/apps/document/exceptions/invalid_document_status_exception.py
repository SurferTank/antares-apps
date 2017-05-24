'''
Created on Jun 17, 2016

@author: leobelen
'''


class InvalidDocumentStatusException(Exception):
    '''
    classdocs
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

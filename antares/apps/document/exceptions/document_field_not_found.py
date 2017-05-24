'''
Created on Jun 19, 2016

@author: leobelen
'''


class DocumentFieldNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

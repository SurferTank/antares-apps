'''
Created on 30/7/2016

@author: leobelen
'''


class ClientException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

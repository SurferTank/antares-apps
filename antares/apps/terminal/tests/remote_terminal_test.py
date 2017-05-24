'''
Created on Jun 23, 2016

@author: leobelen
'''
from django.test import Client
from django.test.testcases import TestCase


class RemoteTerminalTest(TestCase):
    def setup(self):
        self.testClient = Client()
        loginResult = self.testClient.login(
            username='leobelen', password='rabanito')
        assert (loginResult == False)

    def testA(self):
        pass

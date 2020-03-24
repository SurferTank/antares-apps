'''
Created on Oct 2, 2017

@author: leobelen
'''
from antares.apps.document.tests import DocumentTestHelper
from antares.apps.user.models import OrgUnit
from antares.apps.user.models import Role
import logging
import os

from django.test import TransactionTestCase

from ..manager import FlowAdminManager


logger = logging.getLogger(__name__)


class FlowTest(TransactionTestCase):
    """ Test the infrastructure to post a simple document """

    def setUp(self):
        self.docHelper = DocumentTestHelper()
        TransactionTestCase.setUp(self)
        self.xpdl_filename = os.path.join(
                    os.path.dirname(__file__),
                    "workflow.xpdl")
       
    def test_flow_upload(self):
        # seting up a role 
        role = Role()
        role.code = "FLOW_DEFAULT_ROLE"
        role.name = "FLOW_DEFAULT_ROLE"
        role.save()
        
        # unit setup
        unit = OrgUnit()
        unit.code = "DEFAULT_UNIT"
        unit.name = "DEFAULT_UNIT"
        unit.save()
        
        # manager = FlowAdminManager(xpdl_file=self.xpdl_filename)
        # manager.load_xpdl()

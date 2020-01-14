"""
Created on Jul 5, 2016

@author: leobelen
"""
import logging
import os

from django.conf import settings
from django.utils.translation import ugettext as _

from antares.apps.core.constants import FieldDataType
from antares.apps.core.models import SystemParameter
from antares.apps.flow.manager import FlowAdminManager


logger = logging.getLogger(__name__)


class InitialSettingsConsole(object):
    """
        Does the loading of initial data
    """

    @classmethod
    def process_commands(cls, params, html=False):
        """
            Processes the commands defined for initial settings module, 
            so they can be accessible from the web console
        """
        message = ""
        if ('loadxpdl' in params):
            message += cls._load_xpdl(params, html)
        elif ('help' in params):
            message += "We may say that the initial settings help will show up here"
        else:
            message += _(__name__ + ".dont_now_command")

        return message

    @classmethod
    def _load_xpdl(cls, params, html=False):
        """
            Loads an XPDL to Antares
        """
        if ('withpackage' in params):
            package = os.path.join(
                settings.BASE_DIR,
                SystemParameter.find_one(
                    "INITIAL_SETTINGS_DEFAULT_FOLDER", FieldDataType.STRING,
                    'initialsettings'), params['withpackage'], 'flow', 'xpdl')
            if os.path.isdir(package) is False:
                return _(__name__ +
                         ".package_leads_to_inexistent_path {package}").format(
                             package=package)
        else:
            return _(__name__ + ".missing_parameter {parameter}").format(
                parameter='withpackage')

        if ('withfile' in params):
            xpdl_file = os.path.join(package, params['withfile'])
            if os.path.isfile(xpdl_file) is False:
                return _(__name__ + ".package_leads_to_inexistent_file {file}"
                         ).format(file=xpdl_file)
            manager = FlowAdminManager(xpdl_file=xpdl_file)
        else:
            return _(__name__ + ".missing_parameter {parameter}").format(
                parameter='withfile')

        manager.load_xpdl()

        return _(__name__ + ".load_xpdl_sucess")

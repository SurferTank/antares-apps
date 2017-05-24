"""
Created on 30/7/2016

@author: leobelen
"""
import logging

from django.utils.translation import ugettext as _

from antares.apps.core.constants import LanguageType

from ..manager import IsicLoader

logger = logging.getLogger(__name__)


class IsicConsole(object):
    """
        Loads the ISIC standard structure into Antares, based on the language passed. 
    """

    @classmethod
    def process_commands(cls, params, html=False):
        message = ""
        if ('load' in params):
            message += cls._load_isic_file(params, html)
        elif ('help' in params):
            message += "We may say that the isic help will show up here"
        else:
            message += _(__name__ + ".dont_now_command")

        return message

    @classmethod
    def _load_isic_file(cls, params, html):
        """
            Processes the command to load the ISIC files into the system. 
        """
        if 'withlanguage' in params:
            language = LanguageType.to_enum(params['withlanguage'])
            if (language is None):
                return _(__name__ + ".unsupported_language")
            message = IsicLoader.load_isic_file(language)
        else:
            message = _(__name__ + ".missing_parameter {param}").format(
                param="withlanguage")
        return message

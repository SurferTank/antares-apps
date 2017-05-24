"""
Created on 30/7/2016

@author: leobelen
"""
import csv
import logging
import os

from django.utils.translation import ugettext as _

from antares.apps.core.constants import LanguageType

from antares.apps.client.models import IsicPosition
from django.conf import settings
from antares.apps.core.constants import FieldDataType
from antares.apps.core.models import SystemParameter

logger = logging.getLogger(__name__)


class IsicLoader(object):
    """
        Loads the ISIC standard structure into Antares, based on the language passed. 
    """

    @classmethod
    def load_isic_file(cls, language):
        """
            Loads the ISIC file into Antares. 
        """
        message = ""
        folder = os.path.join(
            settings.BASE_DIR,
            SystemParameter.find_one("INITIAL_SETTINGS_DEFAULT_FOLDER",
                                     FieldDataType.STRING, 'initialsettings'),
            'isic', 'files')

        if language == LanguageType.ENGLISH:
            with open(
                    os.path.join(folder, 'ISIC_Rev_4_english_structure.txt'),
                    'r',
                    encoding='utf-8') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                isic_reader = csv.DictReader(csvfile, dialect=dialect)
                for row in isic_reader:
                    if (row['Code'].isalpha()):
                        top_layer = row['Code']
                        IsicPosition.save_position(
                            row['Code'], row['Description'], language)
                    else:
                        IsicPosition.save_position(top_layer + row['Code'],
                                                   row['Description'],
                                                   language)
                message = _(__name__ + ".command_successful")
            return message
        elif language == LanguageType.SPANISH:
            with open(
                    os.path.join(folder, 'ISIC_Rev_4_spanish_structure.txt'),
                    'r',
                    encoding='utf-8') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                isic_reader = csv.DictReader(csvfile, dialect=dialect)
                for row in isic_reader:
                    if (row['Code'].isalpha()):
                        top_layer = row['Code']
                        IsicPosition.save_position(row['Code'], row['Title'],
                                                   language)
                    else:
                        IsicPosition.save_position(top_layer + row['Code'],
                                                   row['Title'], language)
            message = _(__name__ + ".command_successful")
            return message
        else:
            return _(__name__ + ".unsupported_language")

import logging

from django.utils.translation import ugettext as _

from ..constants import SettingsGroupType

logger = logging.getLogger(__name__)


class InitialSettingsLoader(object):
    @classmethod
    def load(cls, settings_group):
        return _(__name__ + ".messages.initial_settings_properly_set")

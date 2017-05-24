import pkgutil
import os
from antares.apps.core.utils import VersionUtils

__path__ = pkgutil.extend_path(__path__, __name__)

VERSION = (0, 0, 1, 'alpha', 0)


def get_version():
    return VersionUtils.get_version(VERSION)

def get_main_version():
    return VersionUtils.get_main_version(VERSION)

def get_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

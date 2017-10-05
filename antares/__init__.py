from antares.apps.core.utils import VersionUtils

VERSION = (0, 0, 1, 'alpha', 0)

def get_version():
    return VersionUtils.get_version()

def get_main_version():
    return VersionUtils.get_main_version()


__version__ = get_main_version()
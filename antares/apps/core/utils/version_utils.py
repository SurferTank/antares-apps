""" based on the excelent DJANGO schema """

import datetime
import functools
import os
import subprocess


class VersionUtils(object):
    @classmethod
    def get_version(cls, version=None):
        """Return a PEP 440-compliant version number from VERSION."""
        version = cls.get_complete_version(version)

        # Now build the two parts of the version number:
        # main = X.Y[.Z]
        # sub = .devN - for pre-alpha releases
        #     | {a|b|rc}N - for alpha, beta, and rc releases

        main = cls.get_main_version(version)

        sub = ''
        if version[3] == 'alpha' and version[4] == 0:
            git_changeset = cls.get_git_changeset()
            if git_changeset:
                sub = '.dev%s' % git_changeset

        elif version[3] != 'final':
            mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
            sub = mapping[version[3]] + str(version[4])

        return main + sub

    @classmethod
    def get_main_version(cls, version=None):
        """Return main version (X.Y[.Z]) from VERSION."""
        version = cls.get_complete_version(version)
        parts = 2 if version[2] == 0 else 3
        return '.'.join(str(x) for x in version[:parts])

    @classmethod
    def get_complete_version(cls, version=None):
        """
        Return a tuple of the django version. If version argument is non-empty,
        check for correctness of the tuple provided.
        """
        if version is None:
            from antares import VERSION as version
        else:
            assert len(version) == 5
            assert version[3] in ('alpha', 'beta', 'rc', 'final')

        return version

    @classmethod
    def get_docs_version(cls, version=None):
        version = cls.get_complete_version(version)
        if version[3] != 'final':
            return 'dev'
        else:
            return '%d.%d' % version[:2]

    @classmethod
    @functools.lru_cache()
    def get_git_changeset(cls):
        """Return a numeric identifier of the latest git changeset.
        The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
        This value isn't guaranteed to be unique, but collisions are very unlikely,
        so it's sufficient for generating the development version numbers.
        """
        repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        git_log = subprocess.Popen(
            'git log --pretty=format:%ct --quiet -1 HEAD',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=repo_dir,
            universal_newlines=True, )
        timestamp = git_log.communicate()[0]
        try:
            timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
        except ValueError:
            return None
        return timestamp.strftime('%Y%m%d%H%M%S')

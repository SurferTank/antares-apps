#!/usr/bin/env python

from distutils.sysconfig import get_python_lib
import os
import sys

from setuptools import setup, find_packages

import antares


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "antares-apps"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break

# Dynamically calculate the version based on django.VERSION.
version = antares.get_main_version()
print('Current version is ' + version)

setup(
    name='antares-apps',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='DUAL',
    description=('Antares Apps Module'),
    long_description=README,
    zip_safe=True,
    download_url='https://bitbucket.org/leobelen/antares-apps/get/' + version +
    '.tar.gz',
    keywords=['management', 'infrastructure'],
    install_requires=[
        'Django >=2.2.9',
        'defusedxml >=0.5.0',
        'django-allauth >=0.32.0',
        'django-angular >=0.8.4',
        'django-bower >=5.2.0'
        'django-braces>=1.11.0',
        'django-ckeditor >=5.2.2',
        'django-datatables-view >=1.14.0',
        'django-enumfields >=0.9.0',
        'django-extensions >=1.7.8',
        'django-fastcgi >= 0.0.1',
        'django-filter >= 1.0.2',
        'django-libs >= 1.67.12',
        'django-markdown-app >= 0.9.1',
        'django-markdown-deux >= 1.0.5',
        'django-mptt >=0.8.7',
        'django-pipeline >= 1.6.12',
        'djangorestframework >= 3.6.2',
        'google-api-python-client >= 1.6.2',
        'googlemaps >= 2.4.6',
        'Js2Py >= 0.44',
        'Markdown >= 2.6.8',
        'markdown2 >= 2.3.4',
        'MarkupSafe >= 1.0',
        'python-dateutil >= 2.6.0',
        'python-slugify >= 1.2.4',
        'tox >= 2.7.0',
        'whitenoise >= 3.3.0',
    ],
    url='http://antares.surfertank.com/',
    author='Leonardo Javier Belén',
    author_email='leobelen@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha', 'Environment :: Web Environment',
        'Framework :: Django', 'Intended Audience :: Developers',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ])

if overlay_warning:
    sys.stderr.write("""
========
WARNING!
========
You have just installed the antares apps over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
antares apps. This is known to cause a variety of problems. You
should manually remove the
%(existing_path)s
directory and re-install antares-apps.
""" % {"existing_path": existing_path})

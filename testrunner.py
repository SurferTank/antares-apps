#!/usr/bin/env python

import django, sys
from django.conf import settings
import os
from django.utils.translation import ugettext_lazy as _
import platform

STATIC_ROOT = '/docs/projects/www/cdbdemo/public/'
DEFAULT_BINARY = "/Users/leobelen/.virtualenvs/antares/bin/python"
DATABASE_USER = 'antares'
DATABASE_PASSWORD = 'antares'
DATABASE_HOST = 'localhost'
DATABASE_PORT = None
DATABASE_ENGINE = 'django.db.backends.postgresql'
#DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
#DATABASE_ENGINE = 'django.contrib.gis.db.backends.postgis'
#DATABASE_ENGINE = 'django.db.backends.mysql'
DATABASE_NAME = 'antares'
TESTSUITE_DATABASE_NAME = 'antares_test'
ATOMIC_REQUESTS = True
STATIC_URL = '/public/'
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

SITE_ID = 1

SECRET_KEY = 'o-9%7@l+z$7t1g$)+jct*m0e90v87%*7o)%mij&9wz_!*3gu=7'
CSRF_MIDDLEWARE_SECRET = 'o-9%7@l+z$7t1g$)+jct*m0e90v87%*7o)%mij&9wz_!*3gu=7'

SESSION_COOKIE_DOMAIN = None

# all settings in debug section should be false in productive environment
# INTERNAL_IPS should be empty in productive environment

VIEW_TEST = True
INTERNAL_IPS = '127.0.0.1'
SKIP_CSRF_MIDDLEWARE = False

SERVER_EMAIL = 'antares@surfertank.com'
EMAIL_HOST = 'localhost'

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# A default site for the apps who need it.

DJANGO_APPS = ('django.contrib.admin', 'django.contrib.auth',
               'django.contrib.contenttypes', 'django.contrib.sessions',
               'django.contrib.messages', 'django.contrib.staticfiles',
               'django.contrib.sites', 'django.contrib.humanize', )

LOCAL_APPS = ('antares.apps.core', 'antares.apps.accounting',
              'antares.apps.client', 'antares.apps.document',
              'antares.apps.flow', 'antares.apps.obligation',
              'antares.apps.initialsettings', 'antares.apps.subscription',
              'antares.apps.notifications', 'antares.apps.thirdparty',
              'antares.apps.user', 'antares.apps.message',
              'antares.apps.terminal', )

THIRD_PARTY_APPS = (
    'mptt',
    'ckeditor',
    'pipeline',
    'djangobower',
    'rest_framework',
    'rest_framework.authtoken',
    'braces',
    'django_libs',
    'markdown_deux',
    'djng',  # django-angular integration
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    'debug_toolbar',
    'django_extensions',
    'django_markdown', )

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ATOMIC_REQUESTS': ATOMIC_REQUESTS,
            'ENGINE': DATABASE_ENGINE,
            'NAME': DATABASE_NAME,
            'USER': DATABASE_USER,
            'PASSWORD': DATABASE_PASSWORD,
            'HOST': DATABASE_HOST,
            'PORT': DATABASE_PORT,
            'TEST': {
                'NAME': TESTSUITE_DATABASE_NAME,
            }
        }
    },
    ROOT_URLCONF='urls',
    INSTALLED_APPS=INSTALLED_APPS,
    MIDDLEWARE_CLASSES=[
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'djng.middleware.AngularUrlMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'antares.apps.core.middleware.request.RequestMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
    ],
    MEDIA_URL='/media/',
    MEDIA_ROOT=os.path.join(BASE_DIR, 'media'),
    STATICFILES_DIRS=(os.path.join(BASE_DIR, 'bower_components'), os.path.join(
        BASE_DIR, "static"), ),
    STATICFILES_STORAGE='pipeline.storage.PipelineStorage',
    STATICFILES_FINDERS=(
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'djangobower.finders.BowerFinder', 'pipeline.finders.PipelineFinder',
        'pipeline.finders.CachedFileFinder', ),
    PIPELINE={
        'PIPELINE_ENABLED':
        False,
        'CSS_COMPRESSOR':
        'pipeline.compressors.NoopCompressor',
        'JS_COMPRESSOR':
        'pipeline.compressors.NoopCompressor',
        'COMPILERS': [
            'pipeline.compilers.coffee.CoffeeScriptCompiler',
            'pipeline.compilers.sass.SASSCompiler',
        ],
        'DISABLE_WRAPPER':
        True,
        'JS_WRAPPER':
        '%s',
        'SASS_COMPILER':
        os.path.join(BASE_DIR, 'node_modules', '.bin', 'sass'),
        'COFFEE_SCRIPT_BINARY':
        os.path.join(BASE_DIR, 'node_modules', '.bin', 'coffee'),
        'JAVASCRIPT': {
            'common_js': {
                'source_filenames':
                ('jquery/dist/jquery.js', 'jquery.cookie/jquery.cookie.js',
                 'select2/dist/js/select2.full.js',
                 'bootstrap-sass/assets/javascripts/bootstrap.js',
                 'bootstrap-toggle/js/bootstrap-toggle.min.js',
                 'jquery/external/sizzle/dist/sizzle.js', 'angular/angular.js',
                 'djng/js/django-angular.js', 'js/core.js', ),
                'output_filename':
                'js/common_js.js',
            },
            'jquery_terminal': {
                'source_filenames':
                ('jquery.terminal/js/jquery.terminal.js',
                 'jquery.terminal/js/jquery.mousewheel-min.js',
                 'angular-terminal/angular-terminal.js', ),
                'output_filename':
                'js/jquery-terminal.js',
            },
            'datatables_js': {
                'source_filenames':
                ('datatables.net/js/jquery.dataTables.js',
                 'datatables.net-bs/js/dataTables.bootstrap.js',
                 'datatables.net-colreorder/js/dataTables.colReorder.js',
                 'datatables.net-fixedcolumns/js/dataTables.fixedColumns.js',
                 'datatables.net-keytable/js/dataTables.keyTable.js',
                 'datatables.net-responsive/js/dataTables.responsive.js',
                 'datatables.net-responsive-bs/js/responsive.bootstrap.js',
                 'datatables.net-scroller/js/dataTables.scroller.js',
                 'datatables.net-select/js/dataTables.select.js',
                 'datatables.net-bs/js/dataTables.bootstrap.js', ),
                'output_filename':
                'js/datatables_js.js',
            },
            'jquery_ui_js': {
                'source_filenames': ('jquery-ui/jquery-ui.js', ),
                'output_filename': 'js/jquery_ui.js',
            },
            'x_editable_js': {
                'source_filenames':
                ('x-editable/dist/bootstrap3-editable/js/bootstrap-editable.js',
                 ),
                'output_filename':
                'js/x_editable.js',
            },
            'ckeditor_js': {
                'source_filenames': ('ckeditor/ckeditor.js',
                                     'ckeditor/skins/kama/skin.js', ),
                'output_filename':
                'js/ckeditor.js',
            },
            'flow_js': {
                'source_filenames': ('js/flow.js', ),
                'output_filename': 'js/flow.js',
            },
            'obligation_panel_js': {
                'source_filenames': ('js/obligation_panel.js', ),
                'output_filename': 'js/obligation_panel.js',
            },
            'accounting_panel_js': {
                'source_filenames': ('js/accounting_panel.js', ),
                'output_filename': 'js/accounting_panel.js',
            },
            'client_panel_js': {
                'source_filenames': ('js/client_panel.js', ),
                'output_filename': 'js/client_panel.js',
            },
            'terminal_panel_js': {
                'source_filenames': ('js/terminal_panel.js', ),
                'output_filename': 'js/terminal_panel.js',
            },
            'document_edit_common_js': {
                'source_filenames': ('js/document_edit_common.js', ),
                'output_filename': 'js/document_edit_common.js',
            },
            'finance_js': {
                'source_filenames': ('js/finance.js', ),
                'output_filename': 'js/finance.js',
            },
        },
        'STYLESHEETS': {
            'common_css': {
                'source_filenames':
                ('bootstrap/dist/css/bootstrap.css',
                 'bootstrap/dist/css/bootstrap-theme.css',
                 'bootstrap-toggle/css/bootstrap-toggle.min.css',
                 'font-awesome/css/font-awesome.css',
                 'select2/dist/css/select2.css',
                 'select2-bootstrap-theme/dist/select2-bootstrap.min.css',
                 'css/web_core.css'),
                'output_filename':
                'css/common_css.css',
                'extra_context': {},
            },
            'jquery_terminal': {
                'source_filenames':
                ('jquery.terminal/css/jquery.terminal.css', ),
                'output_filename': 'css/jquery-terminal.css',
                'extra_context': {},
            },
            'datatables_css': {
                'source_filenames':
                ('datatables.net-bs/css/dataTables.bootstrap.css',
                 'datatables.net-colreorder-bs/css/colReorder.bootstrap.css',
                 'datatables.net-fixedcolumns-bs/css/fixedColumns.bootstrap.css',
                 'datatables.net-keytable-bs/css/keyTable.bootstrap.css',
                 'datatables.net-responsive-bs/css/responsive.bootstrap.css',
                 'datatables.net-scroller-bs/css/scroller.bootstrap.css',
                 'datatables.net-select-bs/css/select.bootstrap.css',
                 'datatables.net-bs/css/dataTables.bootstrap.css', ),
                'output_filename':
                'css/datatables.css',
                'extra_context': {},
            },
            'jquery_ui_css': {
                'source_filenames': ('jquery-ui/themes/base/jquery-ui.css',
                                     'jquery-ui/themes/base/theme.css', ),
                'output_filename':
                'css/jquery_ui.css',
                'extra_context': {},
            },
            'x_editable_css': {
                'source_filenames':
                ('x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css',
                 ),
                'output_filename':
                'css/x_editable.css',
                'extra_context': {},
            },
            'ckeditor_css': {
                'source_filenames': ('ckeditor/skins/kama/editor.css', ),
                'output_filename': 'css/ckeditor.css',
            },
        },
    },
    LOCALE_PATHS=(os.path.join(BASE_DIR, 'locale'), ),
    LANGUAGES=(('en', _('English')), ('es', _('Spanish')), ),
    CKEDITOR_JQUERY_URL=
    '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
    STATIC_ROOT=STATIC_ROOT,
    STATIC_URL=STATIC_URL, )

# Django >= 1.8
django.setup()
from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(['myapp'])
if failures:
    sys.exit(failures)

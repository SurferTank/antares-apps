#!/usr/bin/env python
try:
    import django, sys
    from django.test.runner import DiscoverRunner
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
    # DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
    # DATABASE_ENGINE = 'django.contrib.gis.db.backends.postgis'
    # DATABASE_ENGINE = 'django.db.backends.mysql'
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
    
    DJANGO_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.humanize',
    )
    
    LOCAL_APPS = (
        'antares.apps.core',
        'antares.apps.accounting',
        'antares.apps.client',
        'antares.apps.document',
        'antares.apps.flow',
        'antares.apps.obligation',
        'antares.apps.initialsettings',
        'antares.apps.subscription',
        'antares.apps.notifications',
        'antares.apps.thirdparty',
        'antares.apps.user',
        'antares.apps.message',
        'antares.apps.terminal',
    )
    
    THIRD_PARTY_APPS = (
        'mptt',
        'ckeditor',
        'djangobower',
        'rest_framework',
        'rest_framework.authtoken',
        'braces',
        'django_libs',
        'markdown_deux',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # 'allauth.socialaccount.providers.facebook',
        # 'allauth.socialaccount.providers.google',
        'debug_toolbar',
        'django_extensions',
        'django_markdown'
    )
    
    INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
    
    settings.configure(
        BASE_DIR=os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        BASE_APP_DIR="antares-tests",
        AUTH_USER_MODEL='user.User',
        TEST_MODE=True,
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
        MIDDLEWARE=[
            'django.middleware.cache.UpdateCacheMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'djng.middleware.AngularUrlMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'antares.apps.core.middleware.request.RequestMiddleware',
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            'django.middleware.cache.FetchFromCacheMiddleware',
        ]
        ,
        MEDIA_URL='/media/',
        MEDIA_ROOT=os.path.join(BASE_DIR, 'media'),
        STATICFILES_DIRS=(
            os.path.join(BASE_DIR, 'bower_components'),
            os.path.join(BASE_DIR, "static"),
        ),
        STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
        STATICFILES_FINDERS=(
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'djangobower.finders.BowerFinder',
        ),
        LOGGING={
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse',
                },
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'formatters': {
                'simple': {
                    'format': '[%(asctime)s] %(levelname)s %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'verbose': {
                    'format':
                    '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                    'datefmt':
                    '%Y-%m-%d %H:%M:%S'
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose'
                },
            },
            'loggers': {
                'root': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate': True,
                    'formatter': 'verbose'
                },
                'django': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate': True,
                    'formatter': 'verbose'
                },
                'antares': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'propagate': True,
                },
                'antares.apps.flow': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'propagate': True,
                }
            }
        },
        LOCALE_PATHS=(os.path.join(BASE_DIR, 'locale'),),
        LANGUAGES=(
            ('en', _('English')),
            ('es', _('Spanish')),
        ),
        CKEDITOR_JQUERY_URL=
        '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js',
        STATIC_ROOT=STATIC_ROOT,
        STATIC_URL=STATIC_URL,
        TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.path.join(BASE_DIR, 'antares'), 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                ],
                'libraries': {
                    'accounting_tags':
                    'antares.apps.accounting.templatetags.accounting_tags',
                    'core_tags':
                    'antares.apps.core.templatetags.core_tags',
                    'notification_tags':
                    'antares.apps.notifications.templatetags.notification_tags',
                    'auth_tags':
                    'antares.apps.user.templatetags.auth_tags',
                    'flow_tags':
                    'antares.apps.flow.templatetags.flow_tags',
                },
                "builtins": [
                    'django.templatetags.static',
                    ]
            },
        },
    ]
    )
    
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements.txt")    

django.setup()


def run_tests(*test_args):
    if not test_args:
        test_args = ['antares.apps.flow']
    test_runner = DiscoverRunner(verbosity=5)

    failures = test_runner.run_tests(test_args)
    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])


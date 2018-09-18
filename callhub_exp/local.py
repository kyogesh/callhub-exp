from .settings import *

DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS += ['api',
                   'core',
                   'django_extensions',
                   'django_nose',
                   'rest_framework',
                   'rest_framework.authtoken',
                   ]

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=api,core',
]

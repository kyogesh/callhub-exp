from .settings import *
import django_heroku


DEBUG = False
ALLOWED_HOSTS = ['52.32.181.40', ]
INSTALLED_APPS += ['api',
                   'core',
                   'django_extensions',
                   'django_nose',
                   'rest_framework',
                   'rest_framework.authtoken',
                   ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd6v722740qbkjl',
        'USER': 'pitxnucxavybjg',
        'PASSWORD': 'e8cef8c0e0e9ec29cf8c712c539f67287c32186fc366c130e2a4496f290985c1',
        'HOST': 'ec2-174-129-32-37.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=api,core',
]


django_heroku.settings(locals())
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

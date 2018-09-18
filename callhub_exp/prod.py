from .settings import *
import django_heroku


DEBUG = True
ALLOWED_HOSTS = ['callhub-experiment.herokuapp.com', ]
INSTALLED_APPS = [
    # 'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'core',
    'django_extensions',
    'django_nose',
    'rest_framework',
    'rest_framework.authtoken',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd52ars1jbcmjrl',
        'USER': 'wjparajvcmoqre',
        'PASSWORD': '2d28acfff5b1c005df0d6478c24f7d873c65b9e29f345f6b3fe15a77cad79606',
        'HOST': 'ec2-174-129-18-98.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


# MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware', ]

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=api,core',
]


django_heroku.settings(locals())
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

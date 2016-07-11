# -*- coding: utf-8 -*-

# MINIMAL CONFIGURATION FOR PRODUCTION ENV

# Create your own prod_local.py
# import * this module there and use it like this:
# python manage.py runserver --settings=project.settings.prod_local

from __future__ import unicode_literals

from .base import *


DEBUG = False

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (('Admin', 'anti-ttip-ceta-bewegung@gmx.de'), )

# Secret key generator: https://djskgen.herokuapp.com/
# You should set your key as an environ variable
# SECRET_KEY = os.environ.get("SECRET_KEY", "") # Wurde von mir zum Upload auskommentiert !!!!!!!!!!!!!!!!!!!!!!!

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['ttipprotest.webfactional.com', ]

EMAIL_HOST = 'mail.gmx.net'
EMAIL_HOST_USER = 'anti-ttip-ceta-bewegung@gmx.de'
EMAIL_HOST_PASSWORD = 'tb§oRW3$qL!CLGf42d3t4AVVf(6&oh/XgJG'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'anti-ttip-ceta-bewegung@gmx.de'  # Django default
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # For error notifications

# You can change this to something like 'MyForum <noreply@example.com>'
#DEFAULT_FROM_EMAIL = 'webmaster@localhost'  # Django default
#SERVER_EMAIL = DEFAULT_FROM_EMAIL  # For error notifications

# Extend the Spirit installed apps
# Check out the .base.py file for more examples
INSTALLED_APPS.extend([
    # 'my_app1',
])

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ttipprotest_db',
        'USER': 'chris_ceta',
        'PASSWORD': 'Wel:4D3aG6.dsdE89!+P95k:lRn',
    }
}

# These are all the languages Spirit provides.
# https://www.transifex.com/projects/p/spirit/
gettext_noop = lambda s: s
LANGUAGES = [
    ('de', gettext_noop('German')),
    ('en', gettext_noop('English')),
    ('es', gettext_noop('Spanish')),
    ('fr', gettext_noop('French')),
    ('hu', gettext_noop('Hungarian')),
    ('pl', gettext_noop('Polish')),
    ('pl-pl', gettext_noop('Poland Polish')),
    ('ru', gettext_noop('Russian')),
    ('sv', gettext_noop('Swedish')),
    ('tr', gettext_noop('Turkish')),
    ('zh-hans', gettext_noop('Simplified Chinese')),
]

# Default language
LANGUAGE_CODE = 'de'

# Keep templates in memory
del TEMPLATES[0]['APP_DIRS']
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
]

# Append the MD5 hash of the file’s content to the filename
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

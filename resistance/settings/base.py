# -*- coding: utf-8 -*-
"""
Django settings for running the example of spirit app
"""

from __future__ import unicode_literals

import os
import sys

from spirit.settings import *

# You may override or extend spirit settings below...

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) delete if it is working

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '62d@f6!hg*@x-8*pjpoz^#39whju*$t_#%cu$u_zft+yp!in+a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1:8000',]
''' Ausgeklammert für Miniapp Entwicklung
EMAIL_HOST = 'mail.gmx.net'
EMAIL_HOST_USER = 'grandmas-beautytips@gmx.de'
EMAIL_HOST_PASSWORD = '?^wTvHx\*:bzFL|$=?Edj5~/LUHfJQ~hX,s'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
'''

# Application definition
SITE_ID = 1
# Extend the Spirit installed apps.
# Check out the spirit.settings.py so you do not end up with duplicated apps.
INSTALLED_APPS.extend([
    # django-core
    'django.contrib.sites',
    # third party apps
    'crispy_forms',
    'easy_maps',
    'threadedcomments',
    'django_comments',
    'geopy',
    # 'tagging', this is neccessary for zinnia
    'spirit',
    # my apps
    'bednbreakfast',
    'event',
    'landingpage',
    'transportation',
])


# Easy_maps
EASY_MAPS_CENTER = (50.98, 11.02)

# Comments
COMMENTS_APP = 'threadedcomments'

# same here, check out the spirit.settings.py
MIDDLEWARE_CLASSES.extend([
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
])

TEMPLATES[0]['DIRS'] = [
    os.path.join(BASE_DIR, 'templates'),
]

# same here
TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
])

# same here (we update the Spirit caches)
CACHES.update({
    # 'default': {
    #   'BACKEND': 'my.backend.path',
    # },
})


ROOT_URLCONF = 'resistance.urls'

WSGI_APPLICATION = 'resistance.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'de-DE'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


'''Static umfasst die interne Gestaltung der Website.
    Gestaltung durch den Programmierer'''
STATIC_URL = '/static/'

# STATIC_ROOT verweist auf einen anderen Server. Hier werden die Staticfiles gespeichert
STATIC_ROOT = "/home/crossways/webapps/resistance_static/"
# old: STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_community', 'static_root')

# STATICFILES_DIRS verweist auf Datein in unserem DJANGO-Projekt
# durch 'python manage.py collectstatic' laden wir unsere Projekt-Static-Dateien
# in den ROOT-Ordner
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'our_static'),
)


'''Media umfasst die Uploads von Usern der Website und somit die äußere Gestaltung'''
MEDIA_URL = '/media/'
MEDIA_ROOT = "/home/crossways/webapps/resistance_media/"
# old: MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_community', 'media_root')


'''Protected_Media werden nicht immer, sondern nach Bedarf angezeigt'''
# PROTECTED_MEDIA =


CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Send an email to the site admins
# on error when DEBUG=False,
# log to console on error always.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

import os

from .base import *

DEBUG = True

SITE_ID = 1

PAPERMERGE_CREATE_INBOX = False

DATABASE_ROUTERS = []

INSTALLED_APPS = (
    'rest_framework',
    'knox',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'papermerge.core',
    'papermerge.contrib.admin',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dynamic_preferences',
    # comment the following line if you don't want to use user preferences
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    'mgclipboard'
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mgclipboard.middleware.ClipboardMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'papermerge.test.auth_backends.TestcaseUserBackend',
    'papermerge.core.auth.NodeAuthBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

REST_KNOX = {
    'AUTH_TOKEN_CHARACTER_LENGTH': 32,
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
}


CELERY_BROKER_URL = "memory://"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'CRITICAL'
    },
}

PAPERMERGE_METADATA_PLUGINS = [
    'papermerge.test.metaplugin.Dummy',
]

MEDIA_ROOT = os.path.join(
    PROJ_ROOT,
    "papermerge",
    "test",
    "media"
)

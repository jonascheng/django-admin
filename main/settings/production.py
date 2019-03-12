from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CACHEOPS_DEGRADE_ON_FAILURE = True

# corsheaders
# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_WHITELIST = [
]

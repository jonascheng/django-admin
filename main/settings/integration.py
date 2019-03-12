from .staging import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CACHEOPS_DEGRADE_ON_FAILURE = False

# If True, the whitelist will not be used and all origins will be accepted. Defaults to False.
CORS_ORIGIN_ALLOW_ALL = True

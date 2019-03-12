from .base import * # NOQA

# disable cacheops in test
CACHEOPS_ENABLED = False

# Loogging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)-15s][%(levelname)-5s][%(pathname)s %(module)s.%(funcName)s#%(lineno)d] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        }
    }
}

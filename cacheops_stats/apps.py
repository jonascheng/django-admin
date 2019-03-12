import logging

from cacheops.signals import cache_invalidated, cache_read
from django.apps import AppConfig

logger = logging.getLogger(__name__)


def stats_collector(sender, func, hit, **kwargs):
    # https://github.com/Suor/django-cacheops#keeping-stats
    event = 'hit' if hit else 'miss'
    logger.info(f'{event} cacheops. sender={sender}. func={func}')


def stats_invalidate(sender, obj_dict, **kwargs):
    logger.info(f'invalidate cacheops. sender={sender}. obj_dict={obj_dict}')


class CacheopsStatsConfig(AppConfig):
    name = 'cacheops_stats'

    def ready(self):
        cache_read.connect(stats_collector)
        cache_invalidated.connect(stats_invalidate)

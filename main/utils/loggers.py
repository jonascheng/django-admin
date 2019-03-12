import threading
import logging
import contextlib

logger = logging.getLogger(__name__)


class Annotation(object):
    """Ideally, the annotations are managed by threading. Therefore, the
    annotations will be added into log by AnnotationLogFilter"""

    tls = threading.local()

    @property
    def attrs(self):
        return self.tls.__dict__

    def update(self, *args, **kwargs):
        return self.attrs.update(*args, **kwargs)

    def clear(self):
        return self.attrs.clear()

    def items(self):
        return self.attrs.items()

    @property
    @contextlib.contextmanager
    def scope(self, **kwargs):
        annotation = self.attrs.copy()
        if kwargs:
            self.attrs.update(kwargs)
        yield self
        self.attrs.clear()
        self.attrs.update(annotation)


class AnnotationLogFilter(logging.Filter):
    """
    logger filter for recording user_id, scan_id and any other info we happen to have lying
    around.
    """

    def filter(self, record):
        """
        Applies filtering to the incoming log message.

        This consists of annotating the basic log record with our extra information.
        """

        for k, v in Annotation().items():
            if k not in record.__dict__ and v is not None:
                record.__dict__[k] = v
        return True

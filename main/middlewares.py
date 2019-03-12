from main.utils import loggers


class LogAnnotationMiddleware(object):
    """
    Applies custom log attributes to each request. This allows us to build up
    attributes during the lifetime of a request, such as user_id, etc.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Attach our custom log attribute collector (LogFilter) at the start of a request.
        Ideally this should be one of the earlier middleware components in the stack
        (this can be achieved by listing it towards the end of the entries in settings.py),
        in case any other middleware components have annotations to include.
        """
        request.log_annot = loggers.Annotation()
        with request.log_annot.scope:
            response = self.get_response(request)

        return response

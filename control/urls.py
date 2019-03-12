from django.conf import settings
from django.urls import include, path, re_path

from .views import HealthCheck

urlpatterns = [path('healthcheck', HealthCheck.as_view(), name='health-check')]

if settings.DEBUG:
    from .views import schema_view

    urlpatterns += [
        path(
            'schema/',
            include([
                re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                        schema_view.without_ui()),
                path('swagger', schema_view.with_ui('swagger')),
                path('redoc', schema_view.with_ui('redoc')),
            ]))
    ]

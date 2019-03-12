import logging

from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view

logger = logging.getLogger(__name__)

if settings.DEBUG:
    logger.info('Prepare for schema document')
    schema_view = get_schema_view(
        openapi.Info(
            title=f'{settings.PROJECT_CODE} API Document',
            default_version='v1.0'),
        public=True,
        authentication_classes=(),
        permission_classes=(permissions.AllowAny, ),
    )


class HealthCheck(APIView):
    authentication_classes = ()
    permission_classes = ()
    versioning_class = None

    @swagger_auto_schema(
        operation_description='service health check',
        responses={200: '{"success": true}'})
    def get(self, _):
        return Response({'success': True})

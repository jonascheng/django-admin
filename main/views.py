from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheck(APIView):
    authentication_classes = ()
    permission_classes = ()
    versioning_class = None

    def get(self, _):
        return Response({'success': True})

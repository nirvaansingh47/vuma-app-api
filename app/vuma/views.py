from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import VumaRequest

from vuma.serializers import VumaRequestSerializer


class VumaRequestViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Manage Requests in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = VumaRequest.objects.all()
    serializer_class = VumaRequestSerializer

    def get_queryset(self):
        """Get requests for logged in user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create objects"""
        serializer.save(user=self.request.user)

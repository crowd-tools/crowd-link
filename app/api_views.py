from django.contrib.auth import models as django_models
from rest_framework import permissions
from rest_framework import viewsets

from . import models, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = django_models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = django_models.User.objects.all()
        elif self.request.user.is_authenticated:
            qs = django_models.User.objects.filter(username=self.request.user.username)
        else:
            qs = django_models.User.objects.none()
        return qs.order_by('-date_joined')


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = django_models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = django_models.Group.objects.all()
        else:
            qs = self.request.user.groups.all()
        return qs


class CampaignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows campaigns to be viewed or edited.
    """
    queryset = models.Campaign.objects.all().order_by('-timestamp')
    serializer_class = serializers.CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]


class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed or edited.
    """
    queryset = models.Link.objects.all()
    serializer_class = serializers.LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

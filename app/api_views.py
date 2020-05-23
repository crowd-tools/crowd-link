from django.contrib.auth import models as django_models
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from . import models, serializers
from .views import build_long_link


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = django_models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = django_models.User.objects.all()
        elif self.request.user.is_authenticated:
            qs = django_models.User.objects.filter(username=self.request.user.username)
        else:
            qs = django_models.User.objects.none()
        return qs.order_by('-date_joined')


class CampaignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows campaigns to be viewed or edited.
    """
    queryset = models.Campaign.objects.all().order_by('-timestamp')
    serializer_class = serializers.CampaignSerializer
    permission_classes = []  # TODO split for 2 campaigns PPC & PPS

    def create_link(self, request, pk, *args, **kwargs):
        if 'user_public_key' not in request.data:
            return Response({"error": "'user_public_key' is missing"}, status=400)
        user_public_key = request.data['user_public_key']

        instance = self.get_object()
        try:
            link = instance.links.get(user_public_key=user_public_key)
        except models.Link.DoesNotExist:
            long_link = build_long_link(instance, request, user_public_key)
            link = models.Link.objects.create(
                campaign=instance,
                user_public_key=user_public_key,
                long_link=long_link,
            )

        serializer = serializers.LinkSerializer(link, context={'request': request})
        return Response(serializer.data)


class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed or edited.
    """
    queryset = models.Link.objects.all()
    serializer_class = serializers.LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

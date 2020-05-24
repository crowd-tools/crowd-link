from django.contrib.auth import models as django_models
from django.shortcuts import get_object_or_404
from rest_framework import permissions, views
from rest_framework import viewsets
from rest_framework.response import Response

from . import models, serializers, google_client
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


class CampaignViewSetMixin(viewsets.ModelViewSet):
    """
    API endpoint that allows campaigns to be viewed or edited.
    """
    pass


class SaleCampaignViewSet(CampaignViewSetMixin):
    queryset = models.SaleCampaign.objects.all().order_by('-timestamp')
    serializer_class = serializers.SaleCampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ClickCampaignViewSet(CampaignViewSetMixin):
    queryset = models.ClickCampaign.objects.all().order_by('-timestamp')
    serializer_class = serializers.ClickCampaignSerializer
    permission_classes = []


class SaleLinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed or edited.
    """
    queryset = models.SaleLink.objects.all()
    serializer_class = serializers.SaleLinkSerializer
    permission_classes = []

    def create_link(self, request, pk, *args, **kwargs):
        if 'user_public_key' not in request.data:
            return Response({"error": "'user_public_key' is missing"}, status=400)
        user_public_key = request.data['user_public_key']

        instance = models.SaleCampaign.objects.get(pk=pk)
        try:
            link = instance.links.get(user_public_key=user_public_key)
        except models.SaleLink.DoesNotExist:
            long_link = build_long_link(instance, request, user_public_key)
            link = models.SaleLink.objects.create(
                campaign=instance,
                user_public_key=user_public_key,
                long_link=long_link,
            )

        serializer = serializers.SaleLinkSerializer(link, context={'request': request})
        return Response(serializer.data)


class ClickLinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows links to be viewed or edited.
    """
    queryset = models.ClickLink.objects.all()
    serializer_class = serializers.ClickLinkSerializer
    permission_classes = []

    def create_link(self, request, pk, *args, **kwargs):
        if 'user_public_key' not in request.data:
            return Response({"error": "'user_public_key' is missing"}, status=400)
        user_public_key = request.data['user_public_key']

        instance = models.ClickCampaign.objects.get(pk=pk)
        try:
            link = instance.links.get(user_public_key=user_public_key)
        except models.ClickLink.DoesNotExist:
            long_link = build_long_link(instance, request, user_public_key)
            link = models.ClickLink.objects.create(
                campaign=instance,
                user_public_key=user_public_key,
                long_link=long_link,
            )

        serializer = serializers.ClickLinkSerializer(link, context={'request': request})
        return Response(serializer.data)


class GoogleAnalyticsViewSet(views.APIView):
    def get(self, request, pk):
        campaign = get_object_or_404(models.SaleCampaign, pk=pk)
        if hasattr(campaign.user, 'social_auth'):
            social_auth = campaign.user.social_auth.last()
            client = google_client.GoogleAnalyticsClient(
                access_token=social_auth.extra_data['access_token'],
                refresh_token=social_auth.extra_data.get('refresh_token')
            )
            data = client.get_goal_value(
                view_id=campaign.google_view_id,
                start_date=campaign.timestamp.strftime("%Y-%m-%d"),
            )
            serializer = serializers.GoogleAnalyticsSerializer(data, many=True)
            return Response(serializer.data)
        # This should not happen (let Sentry inform us)

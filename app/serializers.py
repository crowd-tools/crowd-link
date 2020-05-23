from django.contrib.auth import models as django_models
from rest_framework import serializers

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = django_models.User
        fields = ['self_url', 'username', 'first_name', 'last_name', 'email']


class CampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Campaign
        fields = ['self_url', 'name', 'user', 'url', 'reward', 'timestamp']


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Link
        fields = ['self_url', 'user_public_key', 'long_link', 'url_code', 'created']

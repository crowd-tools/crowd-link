from django.contrib.auth import models as django_models
from rest_framework import serializers
from rest_framework.fields import empty

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = django_models.User
        fields = ['self_url', 'username', 'first_name', 'last_name', 'email']


class SaleCampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ['self_url', 'name', 'user', 'url', 'reward', 'timestamp']
        model = models.SaleCampaign


class ClickCampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ['self_url', 'name', 'user_public_key', 'url', 'reward', 'timestamp']
        model = models.ClickCampaign


class SaleLinkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.SaleLink
        fields = ['self_url', 'user_public_key', 'long_link', 'url_code', 'created']
        read_only_fields = ['long_link', 'url_code']


class ClickLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ClickLink
        fields = ['self_url', 'user_public_key', 'long_link', 'url_code', 'created']
        read_only_fields = ['long_link', 'url_code']

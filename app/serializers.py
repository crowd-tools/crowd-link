from django.contrib.auth import models as django_models
from rest_framework import serializers
from rest_framework.fields import empty

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = django_models.User
        fields = ['self_url', 'username', 'first_name', 'last_name', 'email']


class SaleCampaignSerializer(serializers.HyperlinkedModelSerializer):
    links = serializers.SerializerMethodField('get_links')

    class Meta:
        fields = ['self_url', 'name', 'user', 'url', 'reward', 'timestamp', 'links']
        model = models.SaleCampaign
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.update({'user': user})
        return super().create(validated_data)

    def get_links(self, sale_campaign):
        if 'user_public_key' in self.context['request'].GET:
            user_public_key = self.context['request'].GET['user_public_key']
            links = sale_campaign.links.filter(user_public_key=user_public_key)
            serializer = SaleLinkSerializer(links, many=True, context=self.context)
            return serializer.data
        return []


class ClickCampaignSerializer(serializers.HyperlinkedModelSerializer):
    links = serializers.SerializerMethodField('get_links')

    class Meta:
        fields = ['self_url', 'name', 'user_public_key', 'url', 'reward', 'timestamp', 'links']
        model = models.ClickCampaign

    def get_links(self, sale_campaign):
        if 'user_public_key' in self.context['request'].GET:
            user_public_key = self.context['request'].GET['user_public_key']
            links = sale_campaign.links.filter(user_public_key=user_public_key)
            serializer = ClickLinkSerializer(links, many=True, context=self.context)
            return serializer.data
        return []


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

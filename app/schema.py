import graphene
import graphene_django

from . import models


class SaleCampaignType(graphene_django.DjangoObjectType):
    class Meta:
        model = models.SaleCampaign


class ClickCampaignType(graphene_django.DjangoObjectType):
    class Meta:
        model = models.ClickCampaign


class SaleLinkType(graphene_django.DjangoObjectType):
    class Meta:
        model = models.SaleLink


class ClickLinkType(graphene_django.DjangoObjectType):
    class Meta:
        model = models.ClickLink


class Query(object):
    all_sale_campaigns = graphene.List(SaleCampaignType)
    all_click_campaigns = graphene.List(ClickCampaignType)
    all_sale_links = graphene.List(SaleLinkType)
    all_click_links = graphene.List(ClickLinkType)

    def resolve_all_sale_campaigns(self, info, **kwargs):
        return models.SaleCampaign.objects.all()

    def resolve_all_click_campaigns(self, info, **kwargs):
        return models.ClickCampaign.objects.all()

    def resolve_all_sale_links(self, info, **kwargs):
        return models.SaleLink.objects.all()

    def resolve_all_click_links(self, info, **kwargs):
        return models.ClickLink.objects.all()

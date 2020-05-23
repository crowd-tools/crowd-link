from django.contrib import admin

from . import models


@admin.register(models.SaleCampaign)
class SaleCampaignModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'user')


@admin.register(models.ClickCampaign)
class ClickCampaignModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'user_public_key')


@admin.register(models.SaleLink)
class SaleLinkModelAdmin(admin.ModelAdmin):
    list_display = ('long_link', 'user_public_key', 'url_code', 'created')


@admin.register(models.ClickLink)
class ClickLinkModelAdmin(admin.ModelAdmin):
    list_display = ('long_link', 'user_public_key', 'url_code', 'created')

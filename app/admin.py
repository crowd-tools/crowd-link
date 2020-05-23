from django.contrib import admin

from . import models


@admin.register(models.Link)
class LinkModelAdmin(admin.ModelAdmin):
    list_display = ('long_link', 'user_public_key', 'url_code', 'created')


@admin.register(models.Campaign)
class CampaignModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'user')

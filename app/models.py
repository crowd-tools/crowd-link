import uuid

from django.contrib.auth.models import User
from django.db import models


class Campaign(models.Model):
    google_property = models.CharField('GA Property', max_length=15)  # UA-53330308-1
    name = models.CharField('Campaign name', max_length=50, unique=True)
    url = models.URLField('Url of campaign')
    reward = models.DecimalField(default=1, decimal_places=10, max_digits=18)
    user = models.ForeignKey(User, related_name='campaigns', blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)


class Link(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='links', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='links', blank=True, on_delete=models.CASCADE)
    user_public_key = models.CharField('User public key', max_length=42)

    long_link = models.TextField('Long link')
    url_code = models.CharField('URL code', unique=True, blank=True, max_length=12)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'campaign')

    def save(self, *args, **kwargs):
        if not self.id and not self.url_code:
            self.url_code = str(uuid.uuid4())[:8]
        return super().save(*args, **kwargs)

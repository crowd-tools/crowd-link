import uuid

from django.contrib.auth.models import User
from django.core import validators
from django.db import models


class AbstractCamping(models.Model):
    name = models.CharField('Campaign name', max_length=50, unique=True)
    url = models.URLField('Url of campaign')
    reward = models.DecimalField(default=1, decimal_places=10, max_digits=18)
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        abstract = True


class AbstractLink(models.Model):
    user_public_key = models.CharField('User public key', max_length=42, validators=[validators.MinLengthValidator(42)])

    long_link = models.TextField('Long link')
    url_code = models.CharField('URL code', unique=True, blank=True, max_length=12)
    created = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        unique_together = ('user_public_key', 'campaign')
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id and not self.url_code:
            self.url_code = str(uuid.uuid4())[:8]
        return super().save(*args, **kwargs)


class SaleCampaign(AbstractCamping):
    user = models.ForeignKey(User, related_name='campaigns', blank=True, null=True, on_delete=models.SET_NULL)
    user_public_key = models.CharField('User public key', max_length=42, validators=[validators.MinLengthValidator(42)])
    google_view_id = models.CharField('Google View ID', max_length=15)


class ClickCampaign(AbstractCamping):
    user_public_key = models.CharField('User public key', max_length=42, validators=[validators.MinLengthValidator(42)])


class SaleLink(AbstractLink):
    campaign = models.ForeignKey(SaleCampaign, related_name='links', blank=True, on_delete=models.CASCADE)


class ClickLink(AbstractLink):
    campaign = models.ForeignKey(ClickCampaign, related_name='links', blank=True, on_delete=models.CASCADE)

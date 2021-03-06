# Generated by Django 3.0.6 on 2020-05-23 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Campaign name')),
                ('url', models.URLField(verbose_name='Url of campaign')),
                ('reward', models.DecimalField(decimal_places=10, default=1, max_digits=18)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_public_key', models.CharField(max_length=42)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Campaign name')),
                ('url', models.URLField(verbose_name='Url of campaign')),
                ('reward', models.DecimalField(decimal_places=10, default=1, max_digits=18)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaigns', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_public_key', models.CharField(max_length=42, verbose_name='User public key')),
                ('long_link', models.TextField(verbose_name='Long link')),
                ('url_code', models.CharField(blank=True, max_length=12, unique=True, verbose_name='URL code')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='app.SaleCampaign')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClickLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_public_key', models.CharField(max_length=42, verbose_name='User public key')),
                ('long_link', models.TextField(verbose_name='Long link')),
                ('url_code', models.CharField(blank=True, max_length=12, unique=True, verbose_name='URL code')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='app.ClickCampaign')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

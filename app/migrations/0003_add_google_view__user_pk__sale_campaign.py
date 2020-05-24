# Generated by Django 3.0.6 on 2020-05-24 14:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_minlength_validator_for_user_pk'),
    ]

    operations = [
        migrations.AddField(
            model_name='salecampaign',
            name='google_view_id',
            field=models.CharField(default='ga:141873340', max_length=15, verbose_name='Google View ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salecampaign',
            name='user_public_key',
            field=models.CharField(default='0x0', max_length=42, validators=[django.core.validators.MinLengthValidator(42)], verbose_name='User public key'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clickcampaign',
            name='user_public_key',
            field=models.CharField(max_length=42, validators=[django.core.validators.MinLengthValidator(42)], verbose_name='User public key'),
        ),
        migrations.AlterUniqueTogether(
            name='clicklink',
            unique_together={('user_public_key', 'campaign')},
        ),
        migrations.AlterUniqueTogether(
            name='salelink',
            unique_together={('user_public_key', 'campaign')},
        ),
    ]

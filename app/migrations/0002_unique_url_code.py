# Generated by Django 3.0.6 on 2020-05-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='url_code',
            field=models.CharField(blank=True, max_length=12, unique=True, verbose_name='URL code'),
        ),
    ]
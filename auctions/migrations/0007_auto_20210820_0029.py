# Generated by Django 3.2.5 on 2021-08-20 00:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210819_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]

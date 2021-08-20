# Generated by Django 3.2.5 on 2021-08-20 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210820_0029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='bid_value',
            new_name='bid_amount',
        ),
        migrations.AlterField(
            model_name='bids',
            name='listing_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
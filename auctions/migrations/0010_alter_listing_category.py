# Generated by Django 3.2.5 on 2021-09-02 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210820_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Motors', 'Motors'), ('Fashion', 'Fashion'), ('Electronics', 'Electronics'), ('Collectibles and Art', 'Collectibles & Art'), ('Home and Garden', 'Home & Garden'), ('Sporting Goods', 'Sporting Goods'), ('Toys', 'Toys'), ('Business and Industrial', 'Business & Industrial'), ('Music', 'Music')], max_length=25),
        ),
    ]

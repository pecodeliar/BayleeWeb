# Generated by Django 4.2.3 on 2023-10-13 01:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_creator_id_auction_creator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='creation_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 10, 13, 1, 34, 41, 766456, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 10, 13, 1, 34, 41, 766848, tzinfo=datetime.timezone.utc)),
        ),
    ]

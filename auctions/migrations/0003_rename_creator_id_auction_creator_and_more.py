# Generated by Django 4.2.3 on 2023-07-10 00:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_auction_creation_date_alter_bid_creation_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='creator_id',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='auction',
            old_name='image_link',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='user',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='creator',
        ),
        migrations.AlterField(
            model_name='auction',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 0, 44, 42, 463514, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='bid',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 0, 44, 42, 464508, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 10, 0, 44, 42, 464892, tzinfo=datetime.timezone.utc)),
        ),
    ]

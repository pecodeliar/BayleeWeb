# Generated by Django 4.2.3 on 2023-10-14 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_bid_creation_date_bid_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

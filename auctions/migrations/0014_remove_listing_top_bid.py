# Generated by Django 3.0.8 on 2020-07-29 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20200729_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='top_bid',
        ),
    ]

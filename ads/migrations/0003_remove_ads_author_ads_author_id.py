# Generated by Django 4.1.4 on 2022-12-15 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ads_address_alter_ads_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ads',
            name='author',
        ),
        migrations.AddField(
            model_name='ads',
            name='author_id',
            field=models.IntegerField(null=True),
        ),
    ]

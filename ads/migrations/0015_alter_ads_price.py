# Generated by Django 4.1.4 on 2022-12-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0014_remove_users_location_users_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]

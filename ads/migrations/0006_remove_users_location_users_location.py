# Generated by Django 4.1.4 on 2022-12-30 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_users_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='location',
        ),
        migrations.AddField(
            model_name='users',
            name='location',
            field=models.ManyToManyField(null=True, to='ads.location'),
        ),
    ]
# Generated by Django 4.1.4 on 2022-12-15 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_remove_ads_author_ads_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='ads',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
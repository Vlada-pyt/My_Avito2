# Generated by Django 4.1.4 on 2022-12-20 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0012_us'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ads',
            options={'verbose_name': 'Представление', 'verbose_name_plural': 'Представления'},
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Локация', 'verbose_name_plural': 'Локации'},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='ads',
            name='author_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ads.users'),
        ),
        migrations.DeleteModel(
            name='Us',
        ),
    ]
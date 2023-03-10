# Generated by Django 4.1.4 on 2023-01-19 16:54

import ads.validators
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = "True"

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created="True", primary_key="True", serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('password', models.CharField(max_length=200, null=True)),
                ('role', models.CharField(choices=[('member', 'member'), ('moderator', 'moderator'), ('admin', 'admin')], max_length=200)),
                ('age', models.IntegerField(null=True)),
                ('birth_date', models.DateField(blank=True, null=True, validators=[ads.validators.check_birth_date])),
                ('email', models.EmailField(max_length=254, null=True, unique=True, validators=[ads.validators.check_email])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': '????????????????????????',
                'verbose_name_plural': '????????????????????????',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(10)])),
                ('price', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField()),
                ('is_published', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='logos/')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '??????????????????????????',
                'verbose_name_plural': '??????????????????????????',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, unique=True)),
                ('slug', models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(5)])),
            ],
            options={
                'verbose_name': '??????????????????',
                'verbose_name_plural': '??????????????????',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=8, null=True)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=8, null=True)),
            ],
            options={
                'verbose_name': '??????????????',
                'verbose_name_plural': '??????????????',
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('items', models.ManyToManyField(to='ads.ads')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '????????????????',
                'verbose_name_plural': '????????????????',
            },
        ),
        migrations.AddField(
            model_name='ads',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.categories'),
        ),
        migrations.AddField(
            model_name='users',
            name='locations',
            field=models.ManyToManyField(to='ads.location'),
        ),
        migrations.AddField(
            model_name='users',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MinValueValidator

from ads.validators import check_email, check_birth_date


class Categories(models.Model):
    name = models.CharField(unique=True, null=True, max_length=50)
    slug = models.CharField(unique=True, null=True, max_length=10,
                            validators=[MinLengthValidator(5)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    name = models.CharField(max_length=200, null=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')
    ADMIN = 'admin', _('admin')


class Users(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=200, choices=UserRoles.choices)
    age = models.IntegerField(null=True)
    birth_date = models.DateField(validators=[check_birth_date], blank=True, null=True)
    locations = models.ManyToManyField(Location)
    email = models.EmailField(unique=True, null=True, max_length=254, validators=[check_email])
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Ads(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey("Users", related_name="ads", on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    description = models.TextField(null=False)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='logos/', null=True)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Представление"
        verbose_name_plural = "Представления"


class Selection(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Ads)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"


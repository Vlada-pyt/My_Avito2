# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# from ads.models import Location
#
#
# class Users(AbstractUser):
#     first_name = models.CharField(max_length=200, null=True)
#     last_name = models.CharField(max_length=200, null=True)
#     # username = models.CharField(max_length=200, null=True)
#     password = models.CharField(max_length=200, null=True)
#     role = models.CharField(max_length=200)
#     age = models.IntegerField()
#     location = models.ManyToManyField(Location, null=True)
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"

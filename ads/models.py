from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=50)


class Ads(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)


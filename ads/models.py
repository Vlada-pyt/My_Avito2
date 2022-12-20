from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Users(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=200)
    age = models.IntegerField()
    location = models.ManyToManyField(Location, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Ads(models.Model):
    name = models.CharField(max_length=200)
    author_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=1000, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='logos/', null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Представление"
        verbose_name_plural = "Представления"








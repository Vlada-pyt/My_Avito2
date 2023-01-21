import factory

from ads.models import Ads, Categories, Users


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users
    username = factory.Faker("name")


class CategoriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categories
    name = factory.Faker("name")
    slug = factory.Faker("ean", length=8)


class AdsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ads
    name = factory.Faker("name")
    category = factory.SubFactory(CategoriesFactory)
    author = factory.SubFactory(UserFactory)
    price = 100





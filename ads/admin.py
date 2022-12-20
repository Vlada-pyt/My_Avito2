from django.contrib import admin

from ads.models import Categories, Ads, Location, Users

admin.site.register(Categories)
admin.site.register(Ads)
admin.site.register(Location)
admin.site.register(Users)


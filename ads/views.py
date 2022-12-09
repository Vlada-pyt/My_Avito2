from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ads.models import Categories, Ads
from django.views.generic import DetailView
import json

def index(request):
    return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
class CategoriesViews(View):
    def get(self, request):
        categories = Categories.objects.all()

        search_name = request.GET.get('name', None)
        if search_name:
            categories = categories.filter(name=search_name)

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Categories.objects.create(
            name=category_data["name"],
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsViews(View):
    def get(self, request):
        ads = Ads.objects.all()

        search_name = request.GET.get('name', None)
        if search_name:
            ads = ads.filter(name=search_name)

        response = []
        for ad in ads:
            response.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
            })
        return JsonResponse(response, safe=False)


    def post(self, request):
        ads_data = json.loads(request.body)

        ad = Ads.objects.create(
            name=ads_data["name"],
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
        })


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Categories.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })

class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ads.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
        })






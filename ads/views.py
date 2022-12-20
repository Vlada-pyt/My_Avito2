from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ads.models import Categories, Ads, Users
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
import json
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count

def index(request):
    return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesListViews(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_name = request.GET.get('name', None)
        if search_name:
            self.object_list = self.object_list.filter(name=search_name)

        self.object_list = self.object_list.order_by("name")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)


        categories = []
        for category in page_obj:
            categories.append({
                "id": category.id,
                "name": category.name,
            })

        response = {
            "items": categories,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


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


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Categories
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Categories.objects.create(
            name=category_data["name"],
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Categories
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        category_data = json.loads(request.body)

        self.object.name = category_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsListViews(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_name = request.GET.get('name', None)
        if search_name:
            self.object_list = self.object_list.filter(name=search_name)

        self.object_list = self.object_list.order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                'id': ad.id,
                'name': ad.name,
                'author_id': ad.author_id.username,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url,
                'category': ad.category.name,
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
        model = Ads
        fields = ["name", "author_id", "price", "description", "is_published", "image"]

        def post(self, request, *args, **kwargs):
            ad_data = json.loads(request.body)

            ad = Ads.objects.create(
                name=ad_data["name"],
                author_id=ad_data["author_id"],
                price=ad_data["price"],
                description=ad_data["description"],
                is_published=ad_data["is_published"],
                image=ad_data["image"],
            )

            return JsonResponse({
                'id': ad.id,
                'name': ad.name,
                'author_id': ad.author_id.username,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url,
                'category': ad.category.name,
            })

@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ["name", "author_id", "price", "description", "is_published", "image"]

    def post(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]
        self.object.author_id = ad_data["author_id"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.is_published = ad_data["is_published"]
        self.object.image = ad_data["image"]

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.username,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url,
            'category': self.object.category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)



class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ads.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author_id': ad.author_id.username,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url,
            'category': ad.category.name,
        })

@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ["name", "author_id", "price", "description", "is_published", "image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES["image"]

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.username,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url,
            'category': self.object.category.name,

        })


@method_decorator(csrf_exempt, name='dispatch')
class UsersListViews(ListView):
    model = Users

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_name = request.GET.get('username', None)
        if search_name:
            self.object_list = self.object_list.filter(username=search_name)

        self.object_list = self.object_list.order_by("username")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'role': user.role,
                'age': user.age,
                'location': [loc.name for loc in user.location.all()],
                'total_ads': user.ads_set.filter(is_published=True).count()

            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UsersCreateView(CreateView):
        model = Users
        fields = ["first_name", "last_name", "username", "password", "role", "age", "location"]

        def post(self, request, *args, **kwargs):
            user_data = json.loads(request.body)

            user = Users.objects.create(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                username=user_data["username"],
                password=user_data["password"],
                role=user_data["role"],
                age=user_data["age"],
                location=user_data["location"],
            )

            return JsonResponse({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                'location': [loc.name for loc in user.location.all()],
            })

@method_decorator(csrf_exempt, name='dispatch')
class UsersUpdateView(UpdateView):
    model = Ads
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.first_name=user_data["first_name"],
        self.object.last_name=user_data["last_name"],
        self.object.username=user_data["username"],
        self.object.password=user_data["password"],
        self.object.role=user_data["role"],
        self.object.age=user_data["age"],
        self.object.location=user_data["location"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "location": [loc.name for loc in self.object.location.all()],
        })


@method_decorator(csrf_exempt, name='dispatch')
class UsersDeleteView(DeleteView):
    model = Users
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)



class UsersDetailView(DetailView):
    model = Users

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Users.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            'location': [loc.name for loc in user.location.all()],
        })

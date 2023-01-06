from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ads.models import Categories, Ads, Location, Users, Selection
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
import json
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from ads.serializers import UserDetailSerializer, UserListSerializer, UserUpdateSerializer, UserCreateSerializer, \
    LocationModelSerializer, AdsSerializer, AdsListSerializer, AdsDetailSerializer, SelectionSerializer, \
    SelectionListSerializer, SelectionDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.permissions import IsSelectionOwner, IsAdOwnerOrStaff


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


class AdsViewSet(ModelViewSet):
    queryset = Ads.objects.order_by('-price')
    default_serializer = AdsSerializer
    serializer_classes = {
        "List": AdsListSerializer,
        "retrieve": AdsDetailSerializer
    }
    default_permission = [AllowAny()]
    permissions = {
        "retrieve": [IsAuthenticated()],
        "partial_update": [IsAuthenticated(), IsAdOwnerOrStaff()],
        "update": [IsAuthenticated(), IsAdOwnerOrStaff()],
        "delete": [IsAuthenticated(), IsAdOwnerOrStaff()]
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)
        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)
        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author_id__location__name__icontains=location)
        price_from = request.GET.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)
        return super().list(request, *args, **kwargs)


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


class UsersListViews(ListAPIView):
    queryset = Users.objects.annotate(total_ads=Count("ads", filter=Q(ads__is_published=True))).order_by("username")
    serializer_class = UserListSerializer


class UsersCreateView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreateSerializer


class UsersUpdateView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserUpdateSerializer


class UsersDeleteView(DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserDetailSerializer


class UsersDetailView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserDetailSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationModelSerializer


# class SelectionListView(ListAPIView):
#     queryset = Selection.objects.all()
#     serializer_class = SelectionListSerializer
#
#
# class SelectionCreateView(CreateAPIView):
#     queryset = Selection.objects.all()
#     serializer_class = SelectionCreateSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class SelectionUpdateView(UpdateAPIView):
#     queryset = Selection.objects.all()
#     serializer_class = SelectionUpdateSerializer
#     default_permission = [AllowAny()]
#     permissions = {
#         "retrieve": [IsAuthenticated()]
#     }
#
#     def get_permissions(self):
#         return self.permissions.get(self.action, self.default_permission)
#
#
# class SelectionDeleteView(DestroyAPIView):
#     queryset = Selection.objects.all()
#     serializer_class = SelectionDetailSerializer
#     default_permission = [AllowAny()]
#     permissions = {
#         "retrieve": [IsAuthenticated()]
#     }
#
#     def get_permissions(self):
#         return self.permissions.get(self.action, self.default_permission)
#
#
# class SelectionDetailView(RetrieveAPIView):
#     queryset = Selection.objects.all()
#     serializer_class = SelectionDetailSerializer
class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer = SelectionSerializer

    serializer_classes = {
        "list": SelectionListSerializer,
        "retrieve": SelectionDetailSerializer
    }

    default_permission = [AllowAny()]
    permissions = {
        "create": [IsAuthenticated()],
        "retrieve": [IsAuthenticated()],
        "partial_update": [IsAuthenticated(), IsSelectionOwner()],
        "update": [IsAuthenticated(), IsSelectionOwner()],
        "delete": [IsAuthenticated(), IsSelectionOwner()]

    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)







